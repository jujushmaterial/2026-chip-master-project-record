#=============================================================================
# CMP FD-SOI SPAD / Dual-DNW calibration
# SProcess v0.2 - Stage 1: COMMON STI SEED
#
# PURPOSE
#   Run the common front-end only once:
#   SOI definition -> STI etch/fill -> STI densification
#
# OUTPUT
#   n@node@_STI_RESTART_fps.tdr
#
# IMPORTANT
#   - This command contains NO DOE SWB parameters.
#   - The final TDR is explicitly saved with restart information.
#   - Do NOT add !restart, !Gas, or !interfaces to the struct command.
#=============================================================================

set T_USI       0.007
set T_BOX       0.025
set T_STI       0.300

set X_TOP      -0.032
set X_BOX_TOP  -0.025
set X_SURF      0.000
set X_BOT      10.300
set R_DOMAIN   24.00

set T_USI_ETCH [expr 1.001*$T_USI]
set T_BOX_ETCH [expr 1.001*$T_BOX]
set T_STI_ETCH [expr 1.001*$T_STI]

set STI_SEGS {
   0.700  1.300
   2.975  3.275
   6.100  6.400
   9.225  9.525
  12.200 12.800
  17.000 17.600
  18.800 19.400
}

set DENS_T      1000
set DENS_min      20

line clear

line x location=$X_TOP       spacing=0.003  tag=Top
line x location=$X_BOX_TOP   spacing=0.003  tag=BOXTop
line x location=$X_SURF      spacing=0.005  tag=SiTop

line x location=0.100        spacing=0.010
line x location=0.300        spacing=0.010
line x location=0.450        spacing=0.008
line x location=0.700        spacing=0.008
line x location=1.000        spacing=0.015
line x location=1.600        spacing=0.040
line x location=2.500        spacing=0.100
line x location=5.000        spacing=0.400
line x location=$X_BOT       spacing=1.000  tag=SiBottom

line y location=0.000        spacing=0.060  tag=RAxis
line y location=0.550        spacing=0.030
line y location=0.700        spacing=0.030
line y location=1.300        spacing=0.040
line y location=2.975        spacing=0.040
line y location=3.275        spacing=0.040
line y location=6.100        spacing=0.050
line y location=6.400        spacing=0.050
line y location=9.225        spacing=0.050
line y location=9.525        spacing=0.050
line y location=11.800       spacing=0.050
line y location=12.200       spacing=0.030
line y location=12.800       spacing=0.030
line y location=13.200       spacing=0.040
line y location=14.200       spacing=0.050
line y location=15.400       spacing=0.050
line y location=16.300       spacing=0.060
line y location=17.000       spacing=0.050
line y location=17.600       spacing=0.040
line y location=18.800       spacing=0.040
line y location=19.400       spacing=0.050
line y location=$R_DOMAIN    spacing=0.800  tag=ROuter

region Silicon xlo=Top xhi=BOXTop ylo=RAxis yhi=ROuter name=UpperSi
region Oxide   xlo=BOXTop xhi=SiTop ylo=RAxis yhi=ROuter name=BOX
region Silicon xlo=SiTop xhi=SiBottom ylo=RAxis yhi=ROuter        name=Bulk substrate field=Boron concentration=1.0e15<cm-3>

init

mgoals on min.normal.size=3<nm> max.lateral.size=0.50<um>    normal.growth.ratio=1.4

mask clear
mask name=M_STI segments=$STI_SEGS negative

etch Silicon anisotropic thickness=${T_USI_ETCH}<um> mask=M_STI
etch Oxide   anisotropic thickness=${T_BOX_ETCH}<um> mask=M_STI
etch Silicon anisotropic thickness=${T_STI_ETCH}<um> mask=M_STI

deposit Oxide fill coord=${X_TOP}<um> mask=M_STI region.name=STI

grid remesh

diffuse temperature=${DENS_T}<C> time=${DENS_min}<min>
grid remesh

# Remove process-mask state before saving the restart seed.
mask clear

# Explicit restart-capable TDR.
# Sentaurus Process User Guide:
#   TDR restart files preserve geometry/data/PDB/mesh state.
#   !restart, !Gas, or !interfaces would make the file unsuitable
#   for exact split/restart continuation.
struct tdr=n@node@_STI_RESTART restart

puts "=================================================="
puts "COMMON STI SEED COMPLETE"
puts "SEED_NODE=@node@"
puts "SEED_TDR=n@node@_STI_RESTART_fps.tdr"
puts "NEXT_STAGE_MUST_LOAD_THIS_TDR"
puts "=================================================="
