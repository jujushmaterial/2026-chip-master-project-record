# Dual_DNW

## Purpose

This directory contains the current dual-energy DNW calibration flow for the CMP 28 nm FD-SOI SPAD surrogate-baseline reconstruction.

The flow was introduced after analysis of the 250-point Large DOE showed that the single-energy DNW process could reduce the profile RMSE but did not reproduce the SDE baseline DNW width and junction-side tail at the same time.

This directory is a calibration/reconstruction workspace. It is **not** a reconstruction of an ST foundry recipe and it is **not yet** the frozen surrogate baseline.

## Why dual DNW was introduced

The 250-point single-energy DNW DOE showed the following trends inside the sampled parameter space:

- Increasing DNW dose strongly reduced the profile score/RMSE.
- The same dose increase also raised the DNW peak concentration and tended to keep the profile too narrow.
- The best-score candidates still had substantially smaller DNW equivalent sigma than the SDE target.
- Junction-side PActive remained insufficient near the SDE PW/DNW crossing.
- Increasing thermal budget improved PW matching more clearly than DNW width.
- Separate ramp-RTA checks produced only small changes in DNW width and junction-side slope.

Therefore the remaining mismatch was treated as a profile-shape freedom problem rather than something to solve only by increasing RTA or continuing the same single-energy DNW sweep.

## Dual-DNW definition

The DNW is split into two phosphorus implants:

1. **Fixed/Main DNW**
   - Energy: `DNW_E`
   - Dose fraction: `DNW_FIXED_FRAC = 1 - DNW_TRIM_FRAC`
   - Primary role: retain/control the main DNW body and ~1 um peak.

2. **Trim/Assist DNW**
   - Energy: `DNW_TRIM_E`
   - Dose fraction: `DNW_TRIM_FRAC`
   - Primary role: strengthen the shallow/junction-side phosphorus tail and broaden the combined DNW profile.

The total DNW dose remains:

`DNW_DOSE = DNW_FIXED_DOSE + DNW_TRIM_DOSE`

No anneal is inserted between the two DNW implants. Both DNW components, both PW components, and the NW share the same common WELL RTA.

## SWB parameters used by the current split flow

Stage 1 contains no DOE SWB parameters.

Stage 2 uses:

- `DNW_DOSE`
- `DNW_E`
- `DNW_TRIM_E`
- `DNW_TRIM_FRAC`
- `PW_TRIM_E`
- `PW_FIXED_E`
- `PW_TRIM_FRAC`
- `PW_TOTAL_DOSE`
- `RTA_T`
- `RTA_t`

`DNW_FIXED_FRAC`, `DNW_FIXED_DOSE`, `DNW_TRIM_DOSE`, `PW_FIXED_FRAC`, `PW_FIXED_DOSE`, and `PW_TRIM_DOSE` are derived inside the command.

`PW_FIXED_FRAC` is **not** an SWB parameter in this flow. It is calculated internally as `1 - PW_TRIM_FRAC`, so only `PW_TRIM_FRAC` is imported/swept for the PW dose split.

## Files

### CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt

Current recommended Stage 1 for the DOE split/restart flow.

It runs only the common front-end:

`SOI definition -> STI etch/fill -> STI densification`

and saves:

`n@node@_STI_RESTART_fps.tdr`

using:

`struct tdr=n@node@_STI_RESTART restart`

The explicit `restart` option is intentional. Do not add `!restart`, `!Gas`, or `!interfaces`, because those options remove information required for exact Sentaurus Process restart continuation.

### CMP_SPAD_DualDNW_SProcess_v0.2_Stage2_DOE_PLX_only.txt

Current recommended Stage 2 for the 96-case Dual-DNW DOE.

Workbench dependency:

`#setdep @node|sprocess1@`

The stage resolves the upstream seed as:

`n@node|sprocess1@_STI_RESTART_fps.tdr`

and loads it with `init tdr=...`.

A file-existence guard is included. If the Stage 1 restart TDR is not available, Stage 2 stops with an error instead of silently starting from a fresh structure.

Stage 2 intentionally contains none of the following:

- `line clear`
- initial SOI `region` creation
- `M_STI`
- STI silicon/BOX/bulk etch
- STI oxide fill
- STI densification

After the restart load, it begins from the well-mask definitions and Dual-DNW/PW/NW implants.

This split is intended to guarantee that the common STI process is executed once while the 96 DOE branches start from the same post-STI/densification state.



Based on the Large_DOE PLX-only SProcess flow.

Changes from the single-energy Large DOE version are intentionally limited to the DNW module:

- `DNW_DOSE` is interpreted as total DNW dose.
- `DNW_TRIM_E` and `DNW_TRIM_FRAC` are added as SWB parameters.
- `DNW_FIXED_FRAC = 1 - DNW_TRIM_FRAC`.
- The original one-shot DNW implant is replaced by fixed/main + trim/assist phosphorus implants.
- Existing PW, STI, NW, common RTA, PLX outputs, P+ module, contacts, and geometry are preserved.

The command is PLX-first and is intended for calibration screening rather than direct final SDevice use.

### CMP_SPAD_DualDNW_ProfileScreening_SVisualPy_v0.1.py

Dual-DNW profile-screening script.

Detailed metrics remain in the generated metrics text file, but only the following short values are emitted to the SWB DOE table:

- `SCORE`: composite profile-matching score, lower is better. Not percent error.
- `PW_RP`: interior PW main-peak depth [nm].
- `PW_PK_R`: PW peak / SDE PW peak.
- `DNW_RP`: DNW main-peak depth [nm].
- `DNW_PK_R`: DNW peak / SDE DNW peak.
- `DNW_SIG`: DNW equivalent sigma [nm].
- `JUNC`: PW/DNW metallurgical crossing [nm].
- `P462_R`: PActive at the SDE crossing / SDE target PActive.
- `SLOPE_R`: DNW junction-side log-slope / SDE target slope.
- `SPLIT`: two-lobe severity; closer to zero is better.

The composite score uses PW peak/shape, DNW peak/width/shape, crossing, junction-side PActive, junction-side slope, and a split penalty. The post-RTA `A_R_r4p6` profile is the score basis; the final profile is retained for detailed verification.

## SDE comparison targets used in the screening script

- PW peak depth: 109.3 nm
- PW peak concentration: 5.95e17 cm^-3
- PW sigma target: 200 nm
- DNW peak depth: 1017.3 nm
- DNW peak concentration: 3.15e17 cm^-3
- DNW sigma target: 380.6 nm
- Analytic PW/DNW crossing: 462.6966588130754 nm

These are surrogate baseline calibration targets/constraints and must not be represented as proprietary foundry process values.

## Current interpretation rule

Do not select a final candidate by SCORE alone. Review the top-score group together with:

- DNW sigma
- junction-side PActive ratio
- DNW junction-side slope
- split severity
- PW/DNW crossing

After profile screening, selected candidates still require a TDR-enabled SProcess rerun and SDevice verification of VBD and the 15.6 V SCR condition before any surrogate baseline freeze.
