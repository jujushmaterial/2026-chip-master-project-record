# H2 corrected package — static validation report

Date: 2026-11-11

## Included changes

1. `H2_compare_cases.py` final `H2_results.csv` now emits **exactly 14** specified fields in the requested order. All extra Vcommon/field/avalanche/connectivity diagnostic keys are excluded from the final comparison CSV.
2. Fixed a regression in P0 forward-current ratio aggregation: save the baseline before removing internal `_forward_I` from each output record.
3. PEB/SCR SVisualPy analysis creates unique dataset names (`H2_SCR_000`, `H2_PEB_000`), preventing duplicate-object collisions; rejects an incomplete radial sample or missing essential output rather than silently reporting partial maxima.
4. Forward-bias diagnostic co-ramps cathode and substrate to -0.30 V to reduce the substrate-cathode junction-bias confound; records current closure and enforces 1% KCL numerical QA, but **does not auto-certify connectivity**.
5. The 14-column comparison writer validates `Dark_OK`, sampled-field completeness and PEB snapshot identity, forward diagnostic QA, per-condition mask and VBD correspondence, and common-bias I-V interpolation coverage before writing a result file.
6. The `H2_manifest_template.csv` supports optional manual status input for `CathodeConnectivity` and `PEBRisk`. Defaults are `REVIEW_REQUIRED` (no fabricated categorical conclusions).

## Test results

- PASS: SWB-placeholder-substituted Python syntax checks.
- PASS: 6 H2 experiment rows and 15 input SWB parameters; exactly `Mask` varies.
- PASS: final H2 comparison output has 14 columns and 6 rows with test data.
- PASS: P0-relative dark-current reduction and forward-current ratio calculations (synthetic input).
- PASS: failed field sampling is rejected and no partial final CSV is emitted.
- PASS: manual review statuses carry through with only allowed vocabulary.
- PASS: duplicate-name-rejecting mock SVisual accepts the SCR then PEB analyses, using separate names; both output sample CSV and metrics text.

## Not verified

- Actual Sentaurus SProcess/SNMesh/SDevice/SVisualPy run and voltage-sweep convergence.
- Real material-filtered SVisualPy cutline behavior on the installed T-2022.03 Python bridge (Tcl reference supports materials filtering).
- Any actual device measurement or numerical PEB/dark-current improvement.
- A definitive CathodeConnectivity / PEBRisk label before physical review of TDR and current/ionization maps.
- Generated four source-derived H2 decks require the matching checked-out GitHub source in `H2_prepare_decks.py` and must be inspected in the actual Workbench graph before running.
