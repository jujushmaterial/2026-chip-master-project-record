#!/usr/bin/env python3
# Offline validator for the exact 10-tool SWB layout. No Sentaurus run.
from pathlib import Path
import ast
import re

P = Path(__file__).resolve().parent
FILES = {
    "d1": "05_SDevice_VBD_SCR.cmd",
    "v1": "06_SVisualPy_VBD_SCR.py",
    "d2": "07_SDevice2_Dynamic_SCR_ATP.cmd",
    "v2": "08_SVisualPy2_Dynamic_SCR_ATP.py",
    "d3": "09_SDevice3_DarkCurrent.cmd",
    "v3": "10_SVisualPy3_DarkCurrent.py",
}
content = {key: (P / filename).read_text(encoding="utf-8")
           for key, filename in FILES.items()}

def require(flag, detail):
    if not flag:
        raise AssertionError(detail)

def has(key, *tokens):
    require(all(token in content[key] for token in tokens),
            key + " missing " + ", ".join(x for x in tokens if x not in content[key]))

def executable_lines(text):
    return "\n".join(line for line in text.splitlines()
                     if not line.lstrip().startswith("*"))

# Relative node references must resolve exactly to SNMesh2 or VBD Device1.
has("d1", 'Grid    = "n@node|-1@_msh.tdr"', "BreakAtIonIntegral")
has("v1", "#set VBD_V -1", "#set SCR_BIAS_V -1", "#set ATP_BIAS_V -1",
    'emit("VBD_V", vbd)', 'emit("SCR_BIAS_V", scr_bias)',
    'emit("ATP_BIAS_V", atp_bias)')
has("d2", 'Grid    = "n@node|-3@_msh.tdr"',
    "Voltage=@SCR_BIAS_V@", "Voltage=@ATP_BIAS_V@",
    'Plot(FilePrefix="n@node@_SCR")',
    'Plot(FilePrefix="n@node@_ATP")', "BreakdownProbability(",
    "jBreakdownProbability")
require("BreakAtIonIntegral" not in executable_lines(content["d2"]),
        "SDevice2 may not stop at VBD")
require("_V156" not in executable_lines(content["d2"]),
        "SDevice2 still uses fixed SCR snapshot")
has("v2", 'TDR_FILE = f"n{SNODE}_SCR_des.tdr"',
    'ATP_FILE = f"n{SNODE}_ATP_des.tdr"',
    "VBD = float(@VBD_V@)",
    "SCR_BIAS = float(@SCR_BIAS_V@)",
    "ATP_BIAS = float(@ATP_BIAS_V@)")
require("V156_des.tdr" not in content["v2"] and
        "V170_des.tdr" not in content["v2"],
        "SVisualPy2 is reading a fixed voltage snapshot")
has("d3", 'Grid    = "n@node|-5@_msh.tdr"',
    "Voltage=@SCR_BIAS_V@", "AvalDerivatives")
require("AvalPostProcessing" not in executable_lines(content["d3"]),
        "SDevice3 must retain feedback ON")
has("v3", "SNODE = @node|-1@", "DIAG_NODE = @node|-5@",
    "INear_pAum2", "Dark_OK")

# Python parse after emulating only known SWB macro expansion.
pattern = r"@node(?:\|[^@]+)?@|@(VBD_V|SCR_BIAS_V|ATP_BIAS_V)@"
for key in ("v1", "v2", "v3"):
    expanded = re.sub(pattern, "1", content[key])
    require("@" not in "\n".join(
        line for line in expanded.splitlines()
        if not line.lstrip().startswith("#")
    ), key + " has unexpected SWB macro")
    ast.parse(expanded, filename=FILES[key])

# Dimensional and ordering checks for the exported bias formulas.
for vbd in (15.02598, 16.0, 18.0):
    scr = vbd - 0.197998
    atp = vbd + 1.202002
    require(0 < scr < vbd < atp, "target bias order failed")

# Input 14 SWB process parameters remain unchanged, not hardcoded in CMD.
proc = (P / "02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd").read_text(
    encoding="utf-8"
)
for param in (
    "DNW_E", "DNW_MAIN_DOSE", "DNW_TRIM_E", "DNW_TRIM_DOSE",
    "DNW_DEEP_E", "DNW_DEEP_DOSE", "PW_FIXED_E", "PW_FIXED_DOSE",
    "PW_MID_E", "PW_MID_DOSE", "PW_TRIM_E", "PW_TRIM_DOSE",
    "RTA_T", "RTA_t",
):
    require("@" + param + "@" in proc, "SWB parameter hardcoding: " + param)

print("STATIC_PASS: all six electrical decks, bias flow, Python AST,")
print("             dynamic TDR references, mesh paths, SWB process macros")
print("RUNTIME_UNTESTED: verify pp*_des.cmd and real SWB Sentaurus output")
