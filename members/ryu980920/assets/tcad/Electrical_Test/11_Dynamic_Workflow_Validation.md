# CMP SPAD — 6-node workflow acceptance test

## Gate 1: Deck/Tool connections

Strict SWB order after SNMesh2: SDevice1 → SVisualPy1 → SDevice2 → SVisualPy2 → SDevice3 → SVisualPy3.

Expected upstream mesh from SNMesh2: SD1 `n@node|-1@_msh.tdr`, SD2 `n@node|-3@_msh.tdr`, SD3 `n@node|-5@_msh.tdr`.
Expected node source paths: SV1 reads SD1 PLT, SV2 reads SD2 `_SCR_des.tdr` and `_ATP_des.tdr`, SV3 reads SD3 PLT and SD1 diagnostic PLT.

## Gate 2: No fixed-bias SCR/ATP

SV1 should emit three numeric `DOE:` values. SD2 must preprocess `@SCR_BIAS_V@` and `@ATP_BIAS_V@` into numeric `Goal` voltages, with no `When(Contact=... voltage=15.6/17.0)` snapshots.
After convergence, SD2 must generate two different target-state TDRs, and SV2 must use these exact two files.

## Runtime P0 smoke test (required before marking PASS)

1. Run one P0 experiment through SVisualPy1. Verify extracted `VBD_V`, `SCR_BIAS_V`, `ATP_BIAS_V` and associated audit file.
2. With VBD ≈ 15.02598 V, expect SCR bias ≈ 14.827982 V, ATP bias ≈ 16.227982 V. Exact values depend on the rerun VBD extraction.
3. Open SDevice2 preprocessed `pp*_des.cmd`, verify two goals are real numbers rather than `-1` or unresolved `@...@`.
4. Confirm SD2 reaches both goals and writes `_SCR_des.tdr` and `_ATP_des.tdr`. Confirm SV2 outputs `SCR_OK=1` and `ATP_OK=1`, and record SCR center/width and ATP radial map.
5. Confirm SD3 reaches SCR bias (Feedback ON), and SV3 returns `Dark_OK=1` and `INear_pAum2`. 15.6V current may be NA when VBD < 15.6V.
6. Re-run the shared SDE baseline using the unified ATP physics before using the previous B-side `ATP_peak=0.422` as a direct comparator.

**Evidence state:** offline reference and wiring review only. An actual Sentaurus Workbench/T-2022.03 execution is not available in this environment, so runtime PASS has not yet been demonstrated.
