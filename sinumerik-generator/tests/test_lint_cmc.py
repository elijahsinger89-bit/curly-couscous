#!/usr/bin/env python3
"""The CMC lint rules must catch broken output: copy a generated CMC job, break one thing at a time,
expect the named finding. Usage: test_lint_cmc.py <generated f8_cmc_milling dir>"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
fails = []


def lint(d):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'nc_lint.py'), d], capture_output=True, text=True)
    return r.returncode, r.stdout


def case(label, path, old, new, expect):
    tmp = tempfile.mkdtemp(prefix='lintcmc_')
    d = os.path.join(tmp, 'job')
    shutil.copytree(SRC, d)
    p = os.path.join(d, path)
    t = open(p).read()
    if old not in t:
        fails.append(label + ': text to break not found')
        print('FAIL ' + label + ' (text not found)')
        return
    open(p, 'w').write(t.replace(old, new, 1))
    rc, out = lint(d)
    ok = rc == 1 and expect in out
    print(('ok   ' if ok else 'FAIL ') + label)
    if not ok:
        fails.append(label)
        print(out[-800:])
    shutil.rmtree(tmp, ignore_errors=True)


rc, out = lint(SRC)
print(('ok   ' if rc == 0 else 'FAIL ') + 'clean job has no findings')
if rc:
    fails.append('clean')
W = 'WKS/'
case('EXTERN missing', W + 'C_P1_CMC20.SPF', 'EXTERN C_P1_CMC_BACK(STRING[25],INT,INT,INT,VAR INT)\n', '', 'declare it with EXTERN first')
case('EXTERN types wrong', W + 'C_P1_CMC20.SPF', 'EXTERN C_P1_CMC_BACK(STRING[25],INT,INT,INT,VAR INT)', 'EXTERN C_P1_CMC_BACK(STRING[25],INT,INT,INT,INT)', 'does not match PROC')
case('EXTERN for a cycle', W + 'C_P1_CMC20.SPF', 'EXTERN C_P1_CMC_LOG(STRING[180])', 'EXTERN C_P1_CMC_LOG(STRING[180])\nEXTERN L_TOOL_MEAS(STRING[25])', 'cycles need no EXTERN')
case('VAR given a constant', W + 'C_P1_CMC20.SPF', 'C_P1_CMC20_M(LV_E,LV_E2,LV_M,LV_M2,LV_HIT)', 'C_P1_CMC20_M(LV_E,LV_E2,LV_M,LV_M2,0)', 'needs a variable name')
case('probe lowered without MEAS', W + 'C_P1_CMC20_M.SPF', 'G1 MEAS=1 Z=', 'G1 Z=', 'probe lowering without MEAS=1')
case('no $AC_MEA check', W + 'C_P1_CMC20_M.SPF', 'IF ($AC_MEA[1]==1) GOTOF _CM_HIT\n', '', 'must be followed by STOPRE and the $AC_MEA check')
case('no G94 before probing', W + 'C_P1_CMC20_M.SPF', 'G17 G90 G94', 'G17 G90', 'G17 G90 G94 missing')
case('CMC writes nest status', W + 'C_P1_CMC20.SPF', 'CMC_END:\n', 'CMC_END:\nGV_NEST_STATUS[GV_NEST]=3\n', 'CMC must leave nest status')
case('CMC moves GV_NEST', W + 'C_P1_CMC20.SPF', 'CMC_END:\n', 'CMC_END:\nGV_NEST=GV_NEST+1\n', 'CMC must leave nest status')
case('no STOPRE after the cut', W + 'C_P1_CMC20.SPF', 'CALL LV_B\nSTOPRE\n', 'CALL LV_B\n', 'CALL LV_B must be followed by STOPRE')
case('wear added, not absolute', W + 'C_P1_CMC20.SPF', '$TC_DP15[LV_T,LV_D]=R1005', '$TC_DP15[LV_T,LV_D]=$TC_DP15[LV_T,LV_D]+0.002', 'absolute value from R')
case('pass 9 without SETPIECE(0)', W + 'C_P1_CMC20.SPF', 'SETPIECE(0)                        ;the probe', ';SETPIECE(0)', 'pass 9 must follow SETPIECE(0)')
case('status 3 before the CMC step', W + 'A_P1.MPF', 'L_TOOL_LOAD("EM_0500")\n', 'L_TOOL_LOAD("EM_0500")\nLV_I=1\nWHILE (LV_I<=4)\n  GV_NEST_STATUS[LV_I]=3\n  LV_I=LV_I+1\nENDWHILE\n', 'nest status 3 set outside')
case('measure-only cycle with WO number', W + 'C_P1_CMC20_M.SPF', 'CYCLE977(1001,0,', 'CYCLE977(1001,5,', 'needs S_KNUM 0')
case('protection zone without S_SZA', W + 'C_P1_CMC20_M.SPF', ',-1.0000,1.5000,0,', ',-1.0000,0,0,', 'needs S_SZA')
case('arc increment too large', W + 'C_P1_CMC80_M.SPF', ',200,-35,', ',200,-150,', 'S_INCA')
# probe swivel (f10_swivel output next to the CMC job)
SW = os.path.join(os.path.dirname(SRC), 'f10_swivel')
if os.path.isdir(SW):
    SRC = SW
    case('swivel: G54 after the swivel', W + 'C_P1_PROBE.SPF', ';--- Z DATUM: SURFACE (CYCLE978) ---\nD1', ';--- Z DATUM: SURFACE (CYCLE978) ---\nG54 D1', 'G54 selected again after the swivel')
    case('swivel: no CYCLE800() at the end', W + 'C_P1_PROBE.SPF', 'CYCLE800()                         ;swivel back', ';CYCLE800()', 'no CYCLE800() between the swivel and RET')
    case('swivel: CMC measure no CYCLE800() at the end', W + 'C_P1_CMC10_M.SPF', 'CYCLE800()                         ;probe plane off', ';', 'no CYCLE800() between the swivel and RET')
else:
    fails.append('f10_swivel output not found next to ' + SRC)
print()
print('FAILURES: %d' % len(fails) if fails else 'ALL CMC LINT CHECKS PASSED')
sys.exit(1 if fails else 0)
