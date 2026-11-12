#!/usr/bin/env python3
"""Static checks for the NC files the generator emits.

Every rule cites the SINUMERIK ONE manual it comes from:
  NC = NC programming PM 07/2025, MC = Measuring cycles PM 07/2025,
  SV = System variables LM 07/2022.

Usage: nc_lint.py <dir-with-generated-files> [more dirs...]
Exit 0 = clean, 1 = findings.
"""
import os
import re
import sys

KEYWORDS = {
    'STOPRE', 'RET', 'M30', 'M17', 'TRAFOOF', 'LOOP', 'ENDLOOP', 'ENDIF', 'ELSE', 'ENDWHILE',
    'ENDFOR', 'REPEAT', 'M0', 'M1', 'M3', 'M5', 'M6', 'M8', 'M9', 'M19', 'D0', 'D1', 'G54', 'G70', 'G71',
}
# Subprograms / cycles called by name that exist on the control, not in the zip.
EXTERNAL_CALLS = {'CYCLE800', 'CYCLE832', 'CYCLE977', 'CYCLE978', 'BL9908_MOD', 'BL9902',
                  'GROUP_BEGIN', 'GROUP_END', 'MSG', 'WRITE', 'GETEXET', 'SETPIECE', 'CALL'}
LABEL_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):$')
PROG_RE = re.compile(r'^[A-Za-z_][A-Za-z_][A-Za-z0-9_]{0,22}$')
OPS_WORD = {'AND', 'OR', 'NOT', 'XOR', 'B_AND', 'B_OR', 'B_NOT', 'B_XOR', 'DIV', 'MOD'}
FUNCS = {'ABS', 'ROUND', 'TRUNC', 'SQRT', 'SIN', 'COS'}


class Finding(Exception):
    pass


def strip_comment(line):
    """Return the code part of a line (text before ';' outside a string)."""
    out, ins = [], False
    for ch in line:
        if ch == '"':
            ins = not ins
        if ch == ';' and not ins:
            break
        out.append(ch)
    return ''.join(out).strip(), ins


def split_args(s):
    """Split a top-level argument list (no outer parens) on commas."""
    args, depth, ins, cur = [], 0, False, []
    for ch in s:
        if ch == '"':
            ins = not ins
        if not ins:
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
            elif ch == ',' and depth == 0:
                args.append(''.join(cur).strip())
                cur = []
                continue
        cur.append(ch)
    args.append(''.join(cur).strip())
    return args


TOKEN_RE = re.compile(r'\s*(\$[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*|\.\d+|==|<>|<=|>=|<<|[()\[\],<>+\-*/=]|"[^"]*")')


def tokens(s):
    pos, out = 0, []
    while pos < len(s):
        if s[pos].isspace():
            pos += 1
            continue
        m = TOKEN_RE.match(s, pos)
        if not m:
            raise Finding('cannot tokenise near %r' % s[pos:pos + 12])
        out.append(m.group(1))
        pos = m.end()
    return out


def check_condition(toks, where):
    """A condition is an expression only: an operand may never follow an operand
    (that would be a statement after the condition, e.g. 'IF (A==1) M1')."""
    prev_operand = False
    depth = 0
    i = 0
    while i < len(toks):
        t = toks[i]
        up = t.upper()
        if t in ('(', '['):
            if prev_operand and t == '(':
                raise Finding('%s: operand followed by "(" in condition' % where)
            depth += 1
            prev_operand = False
        elif t in (')', ']'):
            depth -= 1
            prev_operand = True
        elif t == ',':
            prev_operand = False
        elif up in OPS_WORD or t in ('==', '<>', '<=', '>=', '<', '>', '+', '-', '*', '/'):
            prev_operand = False
        elif t == '=':
            raise Finding('%s: assignment inside an IF condition (single-line IF with a statement, NC 4.1.5.2)' % where)
        else:
            if prev_operand:
                raise Finding('%s: statement after the IF condition (%r). A one-line IF is only allowed '
                              'with GOTOB/GOTOF/GOTO/GOTOC (NC 4.1.5.2)' % (where, t))
            if up in FUNCS or t.startswith('$') or re.match(r'[A-Za-z_]', t):
                # function call / array var: next "(" or "[" belongs to it
                if i + 1 < len(toks) and toks[i + 1] in ('(', '['):
                    i += 1
                    depth += 1
                    prev_operand = False
                    i += 1
                    continue
            prev_operand = True
        i += 1
    if depth != 0:
        raise Finding('%s: unbalanced brackets in condition' % where)


def num_or_none(s):
    try:
        return float(s)
    except ValueError:
        return None


def lint_file(path, sigs, progs, findings):
    name = os.path.basename(path)
    raw = open(path, 'rb').read()

    def bad(msg, ln=None):
        findings.append('%s%s: %s' % (name, (':%d' % ln) if ln else '', msg))

    try:
        txt = raw.decode('ascii')
    except UnicodeDecodeError:
        bad('non-ASCII bytes in file')
        return
    if '\r' in txt:
        bad('CR characters (files are written with LF)')
    if '\t' in txt:
        bad('tab characters')
    if not txt.endswith('\n'):
        bad('no final newline')
    base = os.path.splitext(name)[0]
    ext = os.path.splitext(name)[1].upper()
    if ext in ('.SPF', '.MPF') and not PROG_RE.match(base):
        bad('program name %r breaks the naming rule (NC 3.3: <=24 chars, A-Z 0-9 _, first two letters/_)' % base)

    lines = txt.split('\n')
    code = []
    for i, l in enumerate(lines, 1):
        c, open_str = strip_comment(l)
        if open_str:
            bad('unbalanced double quote', i)
        if c:
            code.append((i, c))

    labels = {}
    for idx, (ln, c) in enumerate(code):
        m = LABEL_RE.match(c)
        if m:
            lab = m.group(1)
            if len(lab) < 2 or len(lab) > 32:
                bad('label %s length must be 2-32 (NC 4.1.5.2)' % lab, ln)
            if not re.match(r'^[A-Za-z_]{2}', lab):
                bad('label %s must start with two letters/underscores (NC 4.1.5.2)' % lab, ln)
            if lab in labels:
                bad('label %s defined twice' % lab, ln)
            labels[lab] = idx
        elif ':' in c and re.match(r'^[A-Za-z_][A-Za-z0-9_]*:', c):
            bad('label shares a block with other code (keep labels on their own line)', ln)

    stack = []
    seen_exec = False
    proc_seen = False
    for idx, (ln, c) in enumerate(code):
        up = c.upper()
        first = re.match(r'^([A-Za-z_$][A-Za-z0-9_]*)', c)
        head = first.group(1).upper() if first else ''
        where = '%s:%d' % (name, ln)
        try:
            if head == 'PROC':
                if idx != 0:
                    bad('PROC must be the first code line', ln)
                proc_seen = True
                continue
            if head == 'EXTERN' or head == 'EXTERNAL':
                bad('EXTERN found; the framework uses none (NC 4.2.3.2: cycles need no EXTERN)', ln)
            if head == 'DEF':
                if seen_exec:
                    bad('DEF after an executable statement (definitions first, NC 4.1.1.4 / 4.1.7)', ln)
                if stack:
                    bad('DEF inside a check structure (NC 4.1.7)', ln)
                continue
            if LABEL_RE.match(c):
                if stack:
                    bad('label %s inside a check structure (no jumps into structures, NC 4.1.7)' % c[:-1], ln)
                seen_exec = True
                continue
            seen_exec = True
            # ----- check structures -----
            if head == 'IF':
                rest = c[2:].strip()
                jm = re.search(r'\b(GOTOF|GOTOB|GOTOC|GOTO)\b\s+([A-Za-z0-9_]+)\s*$', rest, re.I)
                if jm:
                    cond = rest[:jm.start()].strip()
                    check_condition(tokens(cond), where)
                    if stack:
                        bad('jump inside a check structure; keep jumps at top level (NC 4.1.7)', ln)
                    check_jump(jm.group(1).upper(), jm.group(2), idx, labels, bad, ln)
                else:
                    if re.search(r'\bGOTO[FBC]?\b', rest, re.I):
                        bad('malformed conditional jump', ln)
                    check_condition(tokens(rest), where)
                    stack.append(('IF', ln))
                continue
            if head == 'ELSE':
                if not stack or stack[-1][0] != 'IF':
                    bad('ELSE without IF', ln)
                if c.strip().upper() != 'ELSE':
                    bad('ELSE must stand alone', ln)
                continue
            if head == 'ENDIF':
                if not stack or stack.pop()[0] != 'IF':
                    bad('ENDIF without IF', ln)
                continue
            if head == 'LOOP':
                stack.append(('LOOP', ln))
                continue
            if head == 'ENDLOOP':
                if not stack or stack.pop()[0] != 'LOOP':
                    bad('ENDLOOP without LOOP', ln)
                continue
            if head == 'WHILE':
                check_condition(tokens(c[5:].strip()), where)
                stack.append(('WHILE', ln))
                continue
            if head == 'ENDWHILE':
                if not stack or stack.pop()[0] != 'WHILE':
                    bad('ENDWHILE without WHILE', ln)
                continue
            if len(stack) > 16:
                bad('check structures nested deeper than 16 (NC 4.1.7)', ln)
            # ----- jumps -----
            if head in ('GOTOF', 'GOTOB', 'GOTO', 'GOTOC'):
                if stack:
                    bad('jump inside a check structure (NC 4.1.7)', ln)
                parts = c.split()
                check_jump(head, parts[1] if len(parts) > 1 else '', idx, labels, bad, ln)
                continue
            # ----- calls -----
            cm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)\s*$', c)
            if cm and cm.group(1).upper() in sigs:
                pname = cm.group(1).upper()
                args = split_args(cm.group(2)) if cm.group(2).strip() else []
                params = sigs[pname]
                if len(args) != len(params):
                    bad('%s called with %d args, PROC has %d' % (pname, len(args), len(params)), ln)
                else:
                    for a, (ptype, pnm) in zip(args, params):
                        is_str = a.startswith('"') and a.endswith('"')
                        if ptype.startswith('STRING'):
                            mx = int(re.search(r'\[(\d+)\]', ptype).group(1))
                            if is_str and len(a) - 2 > mx:
                                bad('%s: %s literal longer than %s' % (pname, pnm, ptype), ln)
                            if not is_str and not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', a):
                                bad('%s: %s needs a string' % (pname, pnm), ln)
                        else:
                            if is_str or a == '':
                                bad('%s: %s needs a number' % (pname, pnm), ln)
                            elif ptype == 'INT' and re.match(r'^-?\d*\.\d*$', a):
                                bad('%s: INT %s given a decimal %s' % (pname, pnm, a), ln)
                continue
            if cm and cm.group(1).upper() in ('CYCLE977', 'CYCLE978'):
                check_cycle(cm.group(1).upper(), split_args(cm.group(2)), bad, ln)
                continue
            if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) and up not in KEYWORDS and not re.match(r'^[GMDSHFABCXYZ]\d+$', up):
                # (an address word such as M56 or B0: a letter then digits can
                #  never be a program name, NC naming rules need two letters/_)
                if up in sigs and sigs[up]:
                    bad('%s needs parameters' % up, ln)
                elif up not in progs and up not in EXTERNAL_CALLS:
                    bad('call to %s, which is neither generated nor a known control program' % c, ln)
            if re.search(r'-0\.0+\b(?!\d)', c) and not re.search(r'-0\.0*[1-9]', c):
                bad('negative zero printed', ln)
            if re.search(r'\d[eE][+-]?\d', c):
                bad('C-style exponent in a number', ln)
            mf = re.search(r'\$P_UIFR\[(\d+)', c)
            if mf and int(mf.group(1)) > 99:
                bad('$P_UIFR index above 99 (SV: 0..99)', ln)
        except Finding as e:
            bad(str(e), ln)
    for kind, ln in stack:
        bad('%s opened here is never closed' % kind, ln)
    return code


def check_jump(kind, target, idx, labels, bad, ln):
    if target not in labels:
        bad('jump target %s does not exist' % target, ln)
        return
    t = labels[target]
    if kind == 'GOTOF' and t <= idx:
        bad('GOTOF %s jumps backward' % target, ln)
    if kind == 'GOTOB' and t >= idx:
        bad('GOTOB %s jumps forward' % target, ln)


def check_cycle(cname, a, bad, ln):
    """Positions and values from MC 5.1.5 (CYCLE978) and 5.1.7 (CYCLE977)."""
    if cname == 'CYCLE977':
        if len(a) > 30:
            bad('CYCLE977 has %d args (max 30, MC 5.1.7)' % len(a), ln)
            return
        mvar = a[0]
        if mvar not in ('101', '102', '104', '105', '106'):
            bad('CYCLE977 S_MVAR %s not a WO-correcting hole/spigot/rib/rectangle (MC 5.1.7)' % mvar, ln)
        if a[1] != 'GV_WO[GV_NEST]':
            bad('CYCLE977 S_KNUM must be GV_WO[GV_NEST]', ln)
        fa, tsa, sid, ma = num_or_none(a[7]), num_or_none(a[8]), num_or_none(a[10]), a[13]
        if fa is None or fa <= 0:
            bad('CYCLE977 S_FA (pos 8) must be > 0', ln)
        if tsa != fa:
            bad('CYCLE977 S_TSA (pos 9) must equal S_FA', ln)
        if mvar in ('102', '104', '106') and (sid is None or sid >= 0):
            bad('CYCLE977 outside feature needs a negative S_ID (pos 11) to lower (MC 5.1.7)', ln)
        if mvar in ('101', '105') and sid != 0:
            bad('CYCLE977 inside feature must have S_ID = 0 (pos 11)', ln)
        if mvar == '104' and ma not in ('1', '2'):
            bad('CYCLE977 rib needs S_MA 1 or 2 (pos 14)', ln)
        if mvar in ('101', '102', '104') and (num_or_none(a[4]) or 0) <= 0:
            bad('CYCLE977 S_SETV (pos 5) must be the diameter/width > 0', ln)
        if mvar in ('105', '106') and ((num_or_none(a[5]) or 0) <= 0 or (num_or_none(a[6]) or 0) <= 0):
            bad('CYCLE977 rectangle needs S_SETV0/S_SETV1 (pos 6/7) > 0', ln)
        if len(a) < 27 or a[25] != '1' or a[26] != '0':
            bad('CYCLE977 _DMODE (pos 26) must be 1 and _AMODE (pos 27) 0', ln)
    else:
        if len(a) > 23:
            bad('CYCLE978 has %d args (max 23, MC 5.1.5)' % len(a), ln)
            return
        if a[0] != '100':
            bad('CYCLE978 S_MVAR must be 100 (surface, WO correction)', ln)
        if a[1] != 'GV_WO[GV_NEST]':
            bad('CYCLE978 S_KNUM must be GV_WO[GV_NEST]', ln)
        if a[7] != '3' or a[8] != '2':
            bad('CYCLE978 must measure Z (S_MA=3, pos 8) in the negative direction (S_MD=2, pos 9)', ln)
        if num_or_none(a[5]) != num_or_none(a[6]):
            bad('CYCLE978 S_TSA (pos 7) must equal S_FA (pos 6)', ln)
        if len(a) < 22 or a[20] != '1' or a[21] != '0':
            bad('CYCLE978 _DMODE (pos 21) must be 1 and _AMODE (pos 22) 0', ln)


def design_checks(files, findings):
    """Framework invariants from the plan (restart safety etc.)."""
    def code_of(n):
        out = []
        for l in open(files[n]).read().split('\n'):
            c, _ = strip_comment(l)
            if c:
                out.append(c)
        return out
    if 'L_RUN_NESTS.SPF' in files:
        c = code_of('L_RUN_NESTS.SPF')
        i = c.index('CALL LD_PROG')
        if c[i + 1] != 'STOPRE':
            findings.append('L_RUN_NESTS.SPF: CALL LD_PROG must be followed by STOPRE (restart safety)')
        if c[1] != 'DEF INT LV_TNO':
            findings.append('L_RUN_NESTS.SPF: DEF INT LV_TNO must be the first line after PROC')
        if any('$P_TOOLNO' in x for x in c):
            findings.append('L_RUN_NESTS.SPF: uses $P_TOOLNO (SV: use GETEXET with magazine management)')
    for n in files:
        if n.startswith('A_') and n.endswith('.MPF'):
            c = code_of(n)
            for i, x in enumerate(c):
                if re.match(r'^GV_STEP=\d+$', x) and x != 'GV_STEP=0':
                    if c[i - 1] not in ('STOPRE', 'L_STEP_ERROR'):
                        findings.append('%s: %s not preceded by STOPRE (restart safety)' % (n, x))
            if c[-1] != 'M30':
                findings.append('%s: last code line must be M30' % n)
    if 'C_P1_WO.SPF' in files:
        c = code_of('C_P1_WO.SPF')
        if 'IF (GV_STEP==0)' not in c:
            findings.append('C_P1_WO.SPF: offset writes must be guarded by IF (GV_STEP==0)')
    if 'C_P1_NESTS.SPF' in files:
        c = code_of('C_P1_NESTS.SPF')
        s = c.index('IF (GV_STEP==0)')
        e = c.index('ENDIF', s)
        blk = c[s:e]
        for need in ('GV_PROBE_CHK=0', 'GV_NEST=0'):
            if need not in blk:
                findings.append('C_P1_NESTS.SPF: %s missing from the fresh-start block' % need)


def main(dirs):
    findings = []
    total = 0
    for d in dirs:
        files = {}
        for root, _, names in os.walk(d):
            for n in names:
                if n.upper().endswith(('.SPF', '.MPF', '.DEF')):
                    files[n] = os.path.join(root, n)
        sigs = {}
        progs = set()
        for n, p in files.items():
            progs.add(os.path.splitext(n)[0].upper())
            first = open(p).read().split('\n', 1)[0]
            m = re.match(r'^PROC\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)\s*$', first)
            if m:
                params = []
                for part in split_args(m.group(2)):
                    pm = re.match(r'^(STRING\[\d+\]|INT|REAL)\s+([A-Za-z_][A-Za-z0-9_]*)$', part.strip())
                    if not pm:
                        findings.append('%s: cannot parse PROC parameter %r' % (n, part))
                        continue
                    params.append((pm.group(1), pm.group(2)))
                sigs[m.group(1).upper()] = params
            elif n.startswith('L_') and n.endswith('.SPF') and first.startswith('PROC'):
                findings.append('%s: malformed PROC line' % n)
        before = len(findings)
        for n in sorted(files):
            lint_file(files[n], sigs, progs, findings)
            total += 1
        design_checks(files, findings)
        print('%s: %d files, %d findings' % (d, len(files), len(findings) - before))
    for f in findings:
        print('  ' + f)
    print('TOTAL %d files, %d findings' % (total, len(findings)))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
