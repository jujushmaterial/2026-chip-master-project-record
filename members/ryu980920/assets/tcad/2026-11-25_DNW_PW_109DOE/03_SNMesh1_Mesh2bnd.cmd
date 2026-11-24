#setdep @node|sprocess@

#=============================================================================
# CMP FD-SOI SPAD / B track
# SMesh pass 1: extract boundary from accepted SProcess mesh
# Version 1.2, 2026-09-15
#
# PURPOSE
#   - Reuse the already completed SProcess result.
#   - Extract a boundary representation from n@node|sprocess@_fps.tdr.
#   - Do NOT rerun SProcess.
#
# INPUT
#   n@node|sprocess@_fps.tdr
#
# OUTPUT
#   n@node@_bnd.tdr
#
# NOTE
#   Sentaurus Mesh Mesh2bnd is a Tools operation.
#   Definitions/Placements are intentionally absent in this first pass.
#=============================================================================

Title "CMP SPAD B-track Mesh2bnd pass"

IOControls {
  EnableTools
  inputFile  = "n@node|sprocess@_fps.tdr"
  outputFile = "n@node@_bnd.tdr"
  useDFISEcoordinates
  numThreads = 4
  verbosity  = 2
}

Tools {
  Mesh2bnd
}
