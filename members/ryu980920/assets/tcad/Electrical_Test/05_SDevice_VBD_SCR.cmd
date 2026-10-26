#setdep @node|-1@

* CMP SPAD VBD/SCR calibration SDevice v1.3-PARENTMESH
* 2026-08-28
* Input uses the immediately upstream SMesh node via @node|-1@.
* Physics, ionization-integral VBD definition, solver, and snapshots are
* intentionally kept identical to the 2026-08-27 calibration deck.
* This avoids @node|snmesh@ resolving to the first Mesh2bnd node.
* Common project coordinate: z_if = raw_y - 0.300 um.

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

    Plot(FilePrefix="n@node@_V150" When(Contact="cathode" voltage=15.0))
    Plot(FilePrefix="n@node@_V154" When(Contact="cathode" voltage=15.4))
    Plot(FilePrefix="n@node@_V156" When(Contact="cathode" voltage=15.6))
    Plot(FilePrefix="n@node@_V158" When(Contact="cathode" voltage=15.8))
    Plot(FilePrefix="n@node@_V160" When(Contact="cathode" voltage=16.0))
    Plot(FilePrefix="n@node@_V164" When(Contact="cathode" voltage=16.4))
    Plot(FilePrefix="n@node@_V180" When(Contact="cathode" voltage=18.0))
    Plot(FilePrefix="n@node@_V200" When(Contact="cathode" voltage=20.0))
    Plot(FilePrefix="n@node@_V220" When(Contact="cathode" voltage=22.0))
    Plot(FilePrefix="n@node@_V240" When(Contact="cathode" voltage=24.0))
  }
}
