# H2 Trim DNW radial-mask experiment — candidate decks (NOT run)

Status: **candidate code only, uploaded to `H2_Mask_Sweep` with user approval**. Sentaurus T-2022.03 has NOT been run. Static validation and model assumptions are separate from physical numerical results.

## Purpose / inputs

Six `Mask` [µm] cases: **16.30 (P0), 14.00, 13.00, 12.50, 12.20, 12.00**. This is a [surrogate mask design] study. All other 14 registered SWB implant and common RTA parameters stay P0-fixed **in SWB experiment rows**, NOT by hardcoding a registered parameter in the command files. `@Mask@` is the fifteenth registered SWB input parameter.

The four generated H2 decks are **already included in this folder**, together with all 13 SWB node decks. To regenerate them from the original `Electrical_Test` source, run `python H2_prepare_decks.py /path/to/Electrical_Test --out H2_generated`. The input folder must contain exact original repo files `02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd`, `04_SNMesh2_ProfileMapping.cmd`, `06_SVisualPy_VBD_SCR.py`, `07_SDevice2_Dynamic_SCR_ATP.cmd`. The generator checks each modification anchor exactly once and stops on an unexpected upstream revision. **No original is overwritten.**

Generated files:
- `02_H2_SProcess2_TrimMask.cmd`: Main/Deep DNW retain 16.3 µm; **Trim ONLY** receives `M_DNW_TRIM` with `right=@Mask@` via a variable. PW mask end stays 12.5 µm. Final PLX added at r=12.10/12.35/12.65 µm, existing r=0/4.6875/13.0 remain. Final `n@node@_fps.tdr` unchanged; **no intermediate TDR**.
- `04_H2_SNMesh2_RefinedEdge.cmd`: expand existing PEB refinement r=11.6–16.0 to r=11.6–16.65 µm so P0 Mask=16.3 µm is also inside the refined area. Also extend junction refinement.
- `06_H2_SVisualPy1_VBD_Bias.py`: keeps VBD-relative SCR (98.7467% of VBD), Dark (98.7467%), ATP (107.6086%) and adds near-breakdown **PEB_BIAS_V = 99.9% VBD** as a *non-SWB-input* extracted evaluation variable.
- `07_H2_SDevice2_SCR_PEB_ATP.cmd`: same physical models, extra `n<node>_PEB_des.tdr` snapshot at 99.9% VBD between SCR and ATP. SDevice1 VBD and SDevice3 dark physics remain unchanged.

## Strict 13-node H2 SWB order

1. `sprocess1`: original `01_SProcess1_CommonSTI.cmd`
2. `sprocess`: **generated** `02_H2_SProcess2_TrimMask.cmd`
3. `snmesh1`: original `03_SNMesh1_Mesh2bnd.cmd`
4. `snmesh2`: **generated** `04_H2_SNMesh2_RefinedEdge.cmd`
5. `sdevice1`: original `05_SDevice_VBD_SCR.cmd`
6. `svisualpy1`: **generated** `06_H2_SVisualPy1_VBD_Bias.py`
7. `sdevice2`: **generated** `07_H2_SDevice2_SCR_PEB_ATP.cmd`
8. `svisualpy2`: original `08_SVisualPy2_Dynamic_SCR_ATP.py`
9. `sdevice3`: original `09_SDevice3_DarkCurrent.cmd`
10. `svisualpy3`: original `10_SVisualPy3_DarkCurrent.py`
11. `svisualpy4`: `11_H2_EField_SVisualPy.py`, reads node 7 SDevice2 via `@node|-4@`
12. `sdevice4`: `12_H2_CathodePath_SDevice.cmd`, reads node 4 SNMesh2 via `@node|-8@`
13. `svisualpy5`: `13_H2_CathodePath_SVisualPy.py`, reads node 12 via `@node|-1@`

**IMPORTANT:** `@node|-n@` references assume this exact topology/order. Check preprocessed `pp*_des.cmd`, final upstream paths, and all `#setdep` before launch. Separate branches in the graphical SWB are possible, but then references must be rewritten to match the actual graph.

## Main H2 metrics

1. **Dark Current (TCAD predicted, not measured DCR):** original `INear_pAum2` at each device's `0.987467*VBD`. Compare additionally at a **common absolute bias** `Vcommon = 0.90 * min(VBD of all six cases)` using original SVisualPy3's `n*_dark_py_reverse_IV_components.csv`. This prevents interpreting a drop that only comes from different applied bias as a process improvement. Original 300 K, SRH/Hurkx, BTBT/Hurkx, Avalanche feedback ON are retained. Preserve the P0-to-candidate area convention. **Don't claim experimental or absolute DCR reduction.**
2. **Cathode path:** read **final 2D NetDoping TDR** and confirm silicon N-type corridor (Main/Deep DNW) continuously connects cathode N-Well; examine `eCurrent/Vector`, `eQuasiFermi` in the forward-biased `n*_FWD_des.tdr` (**substrate and cathode co-ramped to −0.30 V to avoid a directly forward-biased substrate/cathode junction**); compare at the same cathode -0.30 V, verify terminal KCL and substrate current. Forward I–V shift **alone** is not a definitive connectivity or resistance measurement because PN junction properties differ. No artificial optical generation or new probe contact is introduced.
3. **Mask/STI5/center E:** `11_H2_EField_SVisualPy.py` scans Silicon-only radial cuts in PEB 99.9% VBD state, reports E-center at r=4.6875 µm, E-STI5 in 12.1–12.9 µm, E-Mask in `Mask±0.25` µm, E-periphery 11.6–16.65 µm. Returns max field **kV/cm**, location r and raw Y depth, plus max AvalancheGeneration and its coordinate. Saves `n*_H2_PEB_samples.csv` for inspecting spatial data. Repeat field output from SCR (98.7467% VBD) to compare progression.
4. **PEB risk:** classify as **suspected peripheral avalanche dominance**, *not* a proven premature edge breakdown. Examine location of avalanche peak and ionization/breakdown paths as voltage approaches VBD. Compare central and peripheral fields and avalanche **at same relative bias**; never use 1.12 as a published field-ratio threshold.
5. **SCR and ATP:** existing SV2 remain secondary viability constraints. Recheck baseline SCR anchoring across candidate relative voltage biases.

SCR and PEB snapshot cutline names are different (`H2_SCR_*` vs `H2_PEB_*`), removing the previous duplicated-name fault. Any failed cut aborts that case instead of reporting misleading maxima.

Silicon-only cutline filtering matters: STI5 is **oxide** for raw Y 0–0.3 µm. Comparing raw maximum electric field inside oxide would misrepresent semiconductor edge field. The sampling is an approximate grid scan; for hot spots narrower than the radial sampling step, refine mesh and radial cuts and compare convergence before publishing a maximum field.

## Files and outputs

SWB CSV: `H2_SWB_6cases_15Params.csv` (6 rows; 15 parameters).

Postprocessor after all 6 experiments: fill real paths and extracted VBD into `H2_manifest_template.csv`, run `python H2_compare_cases.py H2_manifest_template.csv -o H2_results.csv`. Its P0-relative dark-current reduction and field values are quantitative, but `CathodeConnectivity`, `NetDopingContinuity`, and `PEBRisk` deliberately remain **MANUAL REVIEW REQUIRED** until contour/path review, preventing fake pass/fail results.

## Before trusting numbers

- Verify one P0 experiment reproduces the unmodified P0 (VBD and mapped doping) after remeshing; P0 should not drift significantly from the mesh change.
- Check the H2 Process output exists: `n<node>_fps.tdr`, exactly six final PLX per case. Be alert to any source-to-mesh interpolation effects.
- Check `n<node>_SCR_des.tdr`, `n<node>_PEB_des.tdr`, `n<node>_ATP_des.tdr` exist and new extracted `@PEB_BIAS_V@` is positive and < VBD.
- Check new SVisualPy `sv.create_cutline(...,materials=["Silicon"])` and field/avalanche variable names on installed T-2022.03; failure must STOP numeric extraction rather than silently include oxide E.
- Check dark I–V reaches `DARK_BIAS_V`, its KCL and components, and that each candidate is below its own VBD.
- Check that electron-current vector, forward I–V, and the silicon N-type corridor support the **same** connectivity conclusion.
- Check PEB via peak locations and ionization distribution; field ratio alone cannot demonstrate PEB.

## Source and trust

Changes are based on the previously inspected repo `jujushmaterial/2026-chip-master-project-record`, directory `members/ryu980920/assets/tcad/Electrical_Test` (main as of commit `c2930fae400b22d7b69e7790acc18a7241eb985b`), and bundled Sentaurus Device T-2022.03 manual for snapshot/physics/cutline setup. **No Sentaurus binary executed here.** This package is for code review and test run; upload to this dedicated repository folder was approved; do not claim TCAD validation or alter the frozen Electrical_Test source.

## Final H2_results.csv — exact header order (14 columns)

```csv
Mask_um,VBD_V,INear_pAum2,Icommon_pAum2,DarkReduction_Near_pct,DarkReduction_Common_pct,Ecenter_kVcm,ESTI5_kVcm,EMask_kVcm,EMask_r_um,AvalMask_cm3s,ForwardI_RelativeP0,CathodeConnectivity,PEBRisk
```

- `Ecenter_kVcm`: maximum along the reference center radial cut `r=4.6875 µm` (in Silicon, raw depth ≥0.30 µm), **not** a global max over the full active region.
- `ESTI5_kVcm`: maximum in Silicon for 12.10 ≤ r ≤ 12.90 µm; near STI sidewalls, this includes subsurface Si outside the STI as well.
- `EMask_kVcm`: maximum in Silicon inside `Mask±0.25 µm`, `EMask_r_um`: radius where that maximum occurs. The STI5 and Mask windows may overlap, especially for Mask=12–13 µm.
- `AvalMask_cm3s`: largest local `AvalancheGeneration` in the Mask window at **99.9% VBD**. It is not a PEB occurrence probability.
- `INear_pAum2`: current at **98.7467% each candidate's own VBD**, normalized by the same π×12.5² µm² convention as the existing analysis.
- `Icommon_pAum2`: current at 90% of the **lowest VBD across the six H2 cases**, interpolated from each dark I–V sweep. This common voltage is printed in the command-line log and documented here rather than added as a fifteenth column.
- `ForwardI_RelativeP0`: ratio of terminal current magnitudes at −0.30 V in the **co-ramped cathode/substrate diagnostic**. Not a binary proof of a connected DNW path.
- `CathodeConnectivity`: `REVIEW_REQUIRED` until final Net Doping, `eCurrent/Vector`, and `eQuasiFermi` are examined. After review, optionally set one of `CONNECTED`, `DISCONNECTED`, `INCONCLUSIVE` in the manifest.
- `PEBRisk`: `REVIEW_REQUIRED` until field/avalanche location and near-VBD spatial evolution are reviewed. After review, optionally set `LOW`, `ELEVATED`, `INCONCLUSIVE` in the manifest. `LOW` is a relative risk assessment, **not** experimental proof of no PEB.
- **No separate automatically guessed thresholds** for either review field. 99.9%-VBD snapshot is an H2 risk-screening assumption, not confirmed breakdown onset.

Output is written **only after all six rows pass required-value checks**. If a file, field scan, or dark-current interpolation fails, execution raises an error without emitting a partly populated comparison CSV.

## Installation verification caveats

The four original-deck-derived files are included directly in this folder. `H2_prepare_decks.py` is optional for regenerating them from the matching `Electrical_Test` source. After generation, **open each command in Workbench and verify tool links**, then run one Mask=16.3 P0 experiment before the six-case batch. The Python syntax and manifest aggregation can be tested outside Sentaurus, but the actual `sv.create_cutline(materials=["Silicon"])`, TDR field variable spellings, current signs and convergence must be verified on installed Sentaurus T-2022.03.

### Offline verification performed for this corrected package

Run `python test_h2_static.py` to check syntax after placeholder substitution, all six 15-parameter SWB rows, exact 14-column output, calculation of P0-relative reductions and forward-current ratios, error rejection on incomplete field scans, manual-status propagation, and unique SCR-vs-PEB cutline names using a simulated SVisual interface. The simulated inputs in this test are **synthetic and not TCAD outputs**. The installed Sentaurus runtime, convergence, and actual electron-current paths have not been verified here.

The separate cathode diagnostic includes `Goal { Name="substrate" Voltage=-0.30 }` so substrate and cathode track one another during the forward stress; it also checks terminal KCL closure to 1% [numerical QA assumption]. **Neither terminal-current ratio nor this KCL check certifies DNW–Cathode connectivity.** Review the Silicon Net Doping corridor and spatial `eCurrent/Vector` and `eQuasiFermi` before replacing `REVIEW_REQUIRED`.

## Repository layout (2026-11-11)

This directory contains the 13 node decks in the documented order, plus the two CSV templates, comparator, optional generator, static test and validation report. Original `Electrical_Test` files were copied without changing their contents. Execution and TCAD convergence remain unverified.
