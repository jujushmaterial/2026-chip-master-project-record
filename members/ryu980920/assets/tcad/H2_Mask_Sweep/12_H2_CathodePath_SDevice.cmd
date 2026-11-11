#setdep @node|-8@
* H2 forward-bias diagnostic, 12th Workbench node in the H2 13-node graph.
* Grid is SNMesh2 (node -8). This is not a quantitative contact-resistance
* extraction: it tests diode electron-current continuity along the DNW path.
* Compare each Mask candidate against P0 under identical physical conditions.
* During the forward-bias ramp, substrate tracks cathode to avoid directly
* forward-biasing the substrate/Cathode junction (a confounding current path).
* This remains a diagnostic, not proof of uninterrupted N-type connectivity.
* Confirm with Net Doping, eCurrent/Vector and eQuasiFermi in the TDR.
File {
  Grid    = "n@node|-8@_msh.tdr"
  Current = "@plot@"
  Plot    = "@tdrdat@"
  Output  = "@log@"
}
Electrode {
  { Name="anode" Voltage=0.0 }
  { Name="cathode" Voltage=0.0 }
  { Name="substrate" Voltage=0.0 }
}
Physics {
  Temperature=300.0
  Fermi
  EffectiveIntrinsicDensity(OldSlotboom)
  Mobility(
    DopingDependence
    HighFieldSaturation(GradQuasiFermi)
  )
  Recombination( SRH Auger )
}
Plot {
  Doping DonorConcentration AcceptorConcentration
  eDensity hDensity SpaceCharge
  eCurrent/Vector hCurrent/Vector Current/Vector
  eQuasiFermi hQuasiFermi ElectricField/Vector Potential
}
Math {
  Cylindrical
  Extrapolate
  Derivatives
  RelErrControl
  Digits=6
  ErrRef(Electron)=1.0e4
  ErrRef(Hole)=1.0e4
  Iterations=30
  Notdamped=100
  Number_of_Threads=4
  RhsMin=1.0e-15
  ExitOnFailure
}
Solve {
  Coupled(Iterations=200 LineSearchDamping=1.0e-4) { Poisson }
  Coupled { Poisson Electron Hole }
  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-2
    Increment=1.35 Decrement=2.0
    Goal { Name="cathode" Voltage=-0.30 }
    Goal { Name="substrate" Voltage=-0.30 }
  ) {
    Coupled { Poisson Electron Hole }
    CurrentPlot( Time=(Range=(0 1) Intervals=100) )
  }
  Plot(FilePrefix="n@node@_FWD")
}
