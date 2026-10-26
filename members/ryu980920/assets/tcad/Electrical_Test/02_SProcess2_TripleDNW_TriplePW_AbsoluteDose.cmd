#=============================================================================
# CMP 28nm FD-SOI SPAD / Triple-DNW + Triple-PW / Electrical Validation
# Stage 2 v0.5 - ABSOLUTE DOSE PER IMPLANT (NO FRACTIONS)
#
# REQUIRED WORKBENCH TOOL CHAIN:
#   sprocess1 -> sprocess -> snmesh1 -> snmesh2 -> sdevice -> svisualpy
#
# STAGE 1 SEED:   n@node|sprocess1@_STI_RESTART_fps.tdr
# FINAL STAGE 2:  n@node@_fps.tdr
#   SNMesh1: final fps.tdr from this Stage 2 node
#   SNMesh2: SubMesh uses the same Stage 2 final fps.tdr
#
# Registered SWB parameters (14):
# DNW_E DNW_MAIN_DOSE DNW_TRIM_E DNW_TRIM_DOSE DNW_DEEP_E DNW_DEEP_DOSE
# PW_FIXED_E PW_FIXED_DOSE PW_MID_E PW_MID_DOSE PW_TRIM_E PW_TRIM_DOSE
# RTA_T RTA_t
#
# IMPORTANT: PW_FIXED denotes SHALLOW, PW_TRIM denotes DEEP.
# No fraction and no dose allocation logic are used in this deck.
# All SWB parameters, even experiment-fixed ones, use SWB substitution.
# NO re-creation of STI/SOI in Stage 2. ONE common WELL RTA.
# NO claim of proprietary foundry-process reconstruction.
#=============================================================================

#setdep @node|sprocess1@

set SEED_NODE @node|sprocess1@
set SEED_TDR  n${SEED_NODE}_STI_RESTART_fps.tdr

puts "=================================================="
puts "TRIPLE-DNW + TRIPLE-PW DOE FROM COMMON STI RESTART"
puts "SEED_NODE=${SEED_NODE}"
puts "SEED_TDR=${SEED_TDR}"
puts "DOE_NODE=@node@"
puts "=================================================="

if {![file exists $SEED_TDR]} {
   error "Required common STI restart TDR not found: $SEED_TDR"
}

# Load exact post-STI/densification state from Stage 1; do not remake native STIs.
init tdr=$SEED_TDR
mask clear


#=============================================================================
# 0. SWB PARAMETERS -- SIX INDEPENDENT IMPLANT ENERGY/DOSE PAIRS + RTA
#=============================================================================
# Existing SWB field names for Energy are kept to minimize graph changes.
# MAIN DNW: DNW_E; SHALLOW PW: PW_FIXED_E; DEEP PW: PW_TRIM_E.
# IMPORTANT: remove obsolete DNW/PW total-dose and fraction columns in SWB.

# Triple DNW: Phosphorus
set DNW_E          @DNW_E@
set DNW_MAIN_DOSE  @DNW_MAIN_DOSE@
set DNW_TRIM_E     @DNW_TRIM_E@
set DNW_TRIM_DOSE  @DNW_TRIM_DOSE@
set DNW_DEEP_E     @DNW_DEEP_E@
set DNW_DEEP_DOSE  @DNW_DEEP_DOSE@

# Triple PW: Boron, each dose shared between active PW and substrate PW masks
set PW_FIXED_E     @PW_FIXED_E@
set PW_FIXED_DOSE  @PW_FIXED_DOSE@
set PW_MID_E       @PW_MID_E@
set PW_MID_DOSE    @PW_MID_DOSE@
set PW_TRIM_E      @PW_TRIM_E@
set PW_TRIM_DOSE   @PW_TRIM_DOSE@

# Single common well anneal
set RTA_T          @RTA_T@
set RTA_t          @RTA_t@

# Fail-fast for malformed DOE inputs, without computing or overwriting doses.
foreach name {
   DNW_E DNW_TRIM_E DNW_DEEP_E
   DNW_MAIN_DOSE DNW_TRIM_DOSE DNW_DEEP_DOSE
   PW_FIXED_E PW_MID_E PW_TRIM_E
   PW_FIXED_DOSE PW_MID_DOSE PW_TRIM_DOSE
   RTA_T RTA_t
} {
   if {[set $name] <= 0.0} {
      error "Invalid SWB input: $name must be > 0"
   }
}

#=============================================================================
# 1. FIXED SURROGATE-PROCESS CONSTANTS (unchanged from GitHub Stage 2 v0.3)
#=============================================================================

set NW_DOSE 7.75e14
set NW_E    400
set PP_DOSE 8.21e13
set PP_E    5
set SPIKE_T 1050
set SPIKE_t 1.5
set IMP_TILT 7
set IMP_ROT  0
set IMP_MROT 4
set T_USI 0.007
set T_BOX 0.025
set T_USI_ETCH [expr {1.001 * $T_USI}]
set T_BOX_ETCH [expr {1.001 * $T_BOX}]

set LOCAL_BOX_REMOVE_SEGS {
  -0.100  0.550
  12.800 17.000
  17.600 18.800
  19.400 24.100
}

set R_PW_E    12.50
set R_DNW_E   16.30
set R_NW_S    14.20
set R_NW_E    15.40
set R_PPAN_E   0.55
set R_SUBPW_S 17.60
set R_SUBPW_E 18.80
set R_SUBC_S  17.80
set R_SUBC_E  18.60
set AXIS_EXT -0.10
set R_PROFILE_C 4.6875


#=============================================================================
# RESOLVED PARAMETER AUDIT -- NO FRACTION / TOTAL-DOSE CALCULATION
#=============================================================================
puts "=== CMP STAGE 2 ABSOLUTE-DOSE SWB PARAMETERS ==="
foreach name {
   DNW_E DNW_MAIN_DOSE DNW_TRIM_E DNW_TRIM_DOSE DNW_DEEP_E DNW_DEEP_DOSE
   PW_FIXED_E PW_FIXED_DOSE PW_MID_E PW_MID_DOSE PW_TRIM_E PW_TRIM_DOSE
   RTA_T RTA_t
} {
   puts "$name=[set $name]"
}
puts "==============================================="

#=============================================================================
# 2. DOE-STAGE MASKS (preserved)
#=============================================================================

mask name=M_PW      left=$AXIS_EXT   right=$R_PW_E      negative
mask name=M_DNW     left=$AXIS_EXT   right=$R_DNW_E     negative
mask name=M_NW      left=$R_NW_S     right=$R_NW_E     negative
mask name=M_PW_SUB  left=$R_SUBPW_S  right=$R_SUBPW_E   negative


#=============================================================================
# 3. TRIPLE DNW IMPLANT (same process order as v0.3)
#=============================================================================

implant Phosphorus \
   energy=${DNW_E}<keV> \
   dose=${DNW_MAIN_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_DNW

implant Phosphorus \
   energy=${DNW_TRIM_E}<keV> \
   dose=${DNW_TRIM_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_DNW

implant Phosphorus \
   energy=${DNW_DEEP_E}<keV> \
   dose=${DNW_DEEP_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_DNW


#=============================================================================
# 4. TRIPLE PW IMPLANT -- 3 IMPLANTS PER MASK, 2 DISTINCT PW MASKS
#=============================================================================

# Active PW area
implant Boron \
   energy=${PW_FIXED_E}<keV> \
   dose=${PW_FIXED_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW

implant Boron \
   energy=${PW_MID_E}<keV> \
   dose=${PW_MID_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW

implant Boron \
   energy=${PW_TRIM_E}<keV> \
   dose=${PW_TRIM_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW

# Substrate PW area (same 3 doses, spatially separate mask)
implant Boron \
   energy=${PW_FIXED_E}<keV> \
   dose=${PW_FIXED_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW_SUB

implant Boron \
   energy=${PW_MID_E}<keV> \
   dose=${PW_MID_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW_SUB

implant Boron \
   energy=${PW_TRIM_E}<keV> \
   dose=${PW_TRIM_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PW_SUB


#=============================================================================
# 5. N-WELL IMPLANT
#=============================================================================

implant Phosphorus \
   energy=${NW_E}<keV> \
   dose=${NW_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_NW


#=============================================================================
# 6. BEFORE COMMON WELL RTA PLX
#=============================================================================

SetPlxList { BTotal BActive PTotal PActive }
WritePlx n@node@_B_R_r0.plx   y=0.0
WritePlx n@node@_B_R_r4p6.plx y=${R_PROFILE_C}
WritePlx n@node@_B_R_r13.plx  y=13.0


#=============================================================================
# 7. ONE COMMON WELL RTA
#=============================================================================

diffuse temperature=${RTA_T}<C> time=${RTA_t}<s>
grid remesh
WritePlx n@node@_A_R_r0.plx   y=0.0
WritePlx n@node@_A_R_r4p6.plx y=${R_PROFILE_C}
WritePlx n@node@_A_R_r13.plx  y=13.0


#=============================================================================
# 8. LOCAL UpperSi / BOX REMOVAL
#=============================================================================

mask clear
mask name=M_LOCALBOX \
   segments=$LOCAL_BOX_REMOVE_SEGS \
   negative

etch Silicon \
   anisotropic \
   thickness=${T_USI_ETCH}<um> \
   mask=M_LOCALBOX

etch Oxide \
   anisotropic \
   thickness=${T_BOX_ETCH}<um> \
   mask=M_LOCALBOX

grid remesh


#=============================================================================
# 9. SHALLOW P+ CONTACT IMPLANTS
#=============================================================================

mask clear
mask name=M_PP_AN \
   left=$AXIS_EXT \
   right=$R_PPAN_E \
   negative
mask name=M_PP_SUB \
   left=$R_SUBC_S \
   right=$R_SUBC_E \
   negative

implant Boron \
   energy=${PP_E}<keV> \
   dose=${PP_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PP_AN

implant Boron \
   energy=${PP_E}<keV> \
   dose=${PP_DOSE}<cm-2> \
   tilt=${IMP_TILT}<degree> \
   rotation=${IMP_ROT}<degree> \
   mult.rot=${IMP_MROT} \
   mask=M_PP_SUB


#=============================================================================
# 10. FIXED P+ CONTACT ACTIVATION SPIKE (preserved from Stage2 v0.3)
#=============================================================================

diffuse temperature=${SPIKE_T}<C> time=${SPIKE_t}<s>
grid remesh


#=============================================================================
# 11. FINAL PLX (compatible with SVisualPy v1.3.0)
#=============================================================================

SetPlxList { BTotal BActive PTotal PActive }
WritePlx n@node@_F_r0.plx   y=0.0
WritePlx n@node@_F_r4p6.plx y=${R_PROFILE_C}
WritePlx n@node@_F_r13.plx  y=13.0


#=============================================================================
# 12. DIAGNOSTICS
#=============================================================================

select z=BTotal
puts "=== BTotal layers @ r=0 ==="
layers y=0.0
puts "=== BTotal layers @ r=4.6875 ==="
layers y=${R_PROFILE_C}
puts "=== BTotal layers @ r=13 ==="
layers y=13.0

select z=PTotal
puts "=== PTotal layers @ r=0 ==="
layers y=0.0
puts "=== PTotal layers @ r=4.6875 ==="
layers y=${R_PROFILE_C}
puts "=== PTotal layers @ r=13 ==="
layers y=13.0


#=============================================================================
# 13. CONTACTS
#=============================================================================

contact clear
contact box \
   name=anode \
   Silicon \
   xlo=-0.005<um> \
   xhi=0.010<um> \
   ylo=0.00<um> \
   yhi=0.55<um>

contact box \
   name=cathode \
   Silicon \
   xlo=-0.005<um> \
   xhi=0.010<um> \
   ylo=14.20<um> \
   yhi=15.40<um>

contact box \
   name=substrate \
   Silicon \
   xlo=-0.005<um> \
   xhi=0.010<um> \
   ylo=17.80<um> \
   yhi=18.60<um>

contact list

#=============================================================================
# 14. DEVICE-READY FINAL TDR EXPORT
#=============================================================================
# Must be AFTER contacts and final doping/geometry modifications.
# SProcess produces n<node>_fps.tdr; SNMesh1/2 read this exact file.
# Do not use 'restart' here: downstream consumers expect final process TDR.
struct tdr=n@node@

set FINAL_TDR "n@node@_fps.tdr"
if {![file exists $FINAL_TDR]} {
   error "Final SProcess TDR missing (SNMesh input): $FINAL_TDR"
}
puts "ELECTRICAL_HANDOFF_READY=$FINAL_TDR"
puts "SNMESH1_INPUT=$FINAL_TDR"
puts "SNMESH2_SUBMESH_SOURCE=$FINAL_TDR"

puts "=================================================="
puts "TRIPLE-DNW + TRIPLE-PW ELECTRICAL HANDOFF COMPLETE"
puts "SOURCE_SEED=$SEED_TDR"
puts "DOE_NODE=@node@"
puts "=================================================="
