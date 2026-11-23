# 2026-11-23 H1 DNW SCR position / ATP DOE (20 cases)

## Scope and source
- B-track 28 nm FD-SOI SPAD **surrogate process DOE**, not a foundry manufacturing recipe.
- Today's research timeline: [2026-11-23.md](../../../timeline/2026-11/2026-11-23.md).
- Local user-provided source files analyzed: `1121_H1.csv` (PW 12-case SWB results), `1116-H1.csv` (DNW Trim 9-case SWB results), `n21_SCR_des.tdr` (n21 spatial field/profile); only the **extracted PW metrics** and newly planned DNW DOE are published here, not the original TDR.
- `PW_1121_H1_12case_extracted_metrics.csv`: lossless precision for the selected metric columns; blank I90/Dark_OK denotes **not extracted**, not zero or failure in physical performance.
- The previous H1 P0 (DNW Trim 550 keV / 7.5e12) is distinct from today's **n21 starting condition** (DNW Trim 680 keV / 5.5e12; PW deep 125 keV / 3.24e12).

## DOE: 16 trim-factorial + 4 whole-energy shift
- T01–T16: `DNW_TRIM_E` = 680 / 660 / 640 / 600 keV, `DNW_TRIM_DOSE` = 5.50 / 6.00 / 6.50 / 7.00 e12 cm^-2 (all combinations). `DNW_E`=955 keV, `DNW_DEEP_E`=1485 keV.
- A01–A04: coupled `DNW_TRIM_E / DNW_E / DNW_DEEP_E` = 660/925/1440, 640/900/1400, 620/875/1360, 600/850/1320 keV; all at Trim Dose 5.50e12 cm^-2. A03/A04 are newly extended exploratory assumptions.
- Other constant SWB experiment-row values: DNW Main Dose 1.50e13 cm^-2, DNW Deep Dose 7.00e12 cm^-2; PW Fixed 36 keV / 6.36e12, PW Mid 80 keV / 8.00e12, PW Trim (Deep) 125 keV / 3.24e12; **common** RTA 1050°C / 30 s.
- No process command changes; ALL fourteen registered SWB parameters must stay `@PARAMETER@` in SProcess decks, including fixed variables.

## Files and import
- `DNW_20cases_SWB_Master_NoIndex.csv` — 20 × 14 SWB parameter values.
- `DNW_20cases_Batch1_6cases_SWB_NoIndex.csv` — rows 1–6.
- `DNW_20cases_Batch2_7cases_SWB_NoIndex.csv` — rows 7–13.
- `DNW_20cases_Batch3_7cases_SWB_NoIndex.csv` — rows 14–20.
- `DNW_20cases_CaseMap.csv` — case IDs / row numbering (NOT for SWB import).
- All SWB input CSVs have 14 headers, NO Index/Batch/Case column. Check preprocessing for complete parameter substitution and node dependencies.

## Evaluation and pending tasks
- SCR at r=4.6875 µm; junction zero crossing, E=1e5 V/cm upper/lower crossings, SCR center and width (interface-depth axis).
- Calculate shift of **both** SCR boundaries rather than inferring narrower SCR from a shallower SCR center.
- Examine field and impact-ionization spatial paths near 180 nm, ATP at r-axis / active region, edge onset and PEB, reverse dark current, VBD.
- SWB uses SCR bias VBD×(1−1.2533%), ATP bias VBD×(1+7.6086%) per active SVisualPy settings. Re-evaluate finalists at common **absolute excess bias** and consistent physics before claiming a process ATP advantage.
- Original 2D SDE R0: VBD≈15.798 V, SCR center 180.202945597 nm and width 341.365736988 nm at 15.6 V. n21 SCR is at approximately 15.662 V, so raw center/width differences are not controlled fixed-bias effects.
- **Status: DOE files prepared, zero new 20-case TCAD runs completed in this task**.
