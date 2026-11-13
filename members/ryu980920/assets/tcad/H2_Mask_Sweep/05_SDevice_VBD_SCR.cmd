#setdep @node|-1@

* H2 SDevice1 - VBD extraction, SDE static-baseline physics aligned
* Source of physics/math: CMP_SPAD_VBD_Diagnostic_SDevice_v1.1_dependency_fix.txt
* H2-specific direct upstream mesh dependency and dynamic SV1 workflow retained.
* Model: standard SRH + Auger + vanOverstraeten GradQuasiFermi.
* No Hurkx TAT/BTBT here, matching the SDE baseline VBD deck.

File {
  Grid    = "n@node|-1@_msh.tdr"
  Current = "@plot@"
  Plot    = "@tdrdat@"
  Output  = "@log@"
}

Electrode {
  { Name="anode"     Voltage=0.0 }
  { Name="cathode"   Voltage=0.0 }
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
  Recombination(
    SRH
    Auger
    Avalanche(vanOverstraeten GradQuasiFermi)
  )
}

Plot {
  Doping DonorConcentration AcceptorConcentration
  eDensity hDensity SpaceCharge
  ElectricField/Vector Potential
  eCurrent/Vector hCurrent/Vector Current/Vector
  eMobility hMobility
  eAlphaAvalanche hAlphaAvalanche
  AvalancheGeneration
  eIonIntegral hIonIntegral MeanIonIntegral
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

  AvalPostProcessing
  BreakAtIonIntegral

  ComputeIonizationIntegrals(
    MinElectricField=1.0e5
    direction="eGradQuasiFermi"
  )
}

Solve {
  Coupled(Iterations=200 LineSearchDamping=1.0e-4) { Poisson }
  Coupled { Poisson Electron Hole }

  Plot(FilePrefix="n@node@_V000")

  Quasistationary(
    InitialStep=1.0e-3
    MinStep=1.0e-8
    MaxStep=2.0e-2
    Increment=1.35
    Decrement=2.0
    Goal { Name="cathode" Voltage=14.0 }
  ){
    Coupled { Poisson Electron Hole }
  }

  Quasistationary(
    InitialStep=1.0e-3
    MinStep=1.0e-9
    MaxStep=2.0e-3
    Increment=1.25
    Decrement=2.0
    Goal { Name="cathode" Voltage=25.0 }
  ){
    Coupled { Poisson Electron Hole }
  }
}
