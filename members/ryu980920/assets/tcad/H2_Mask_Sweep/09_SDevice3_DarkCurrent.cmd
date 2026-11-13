#setdep @node|-1@
#setdep @node|-5@

* H2 SDevice3 - feedback-ON relative dark current at dynamic VBD-derived bias
* Physics/Math aligned to SDE baseline CMP_SPAD_DarkCurrent_SDevice.txt
* H2-specific mesh dependency, dynamic DARK_BIAS_V, and output naming retained.
* Without lifetime/trap calibration, interpret as relative dark current/DCR proxy.

File {
  Grid    = "n@node|-5@_msh.tdr"
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
  AreaFactor=1.0

  Fermi
  EffectiveIntrinsicDensity(OldSlotboom)

  Mobility(
    DopingDependence
    HighFieldSaturation(GradQuasiFermi)
    Enormal
  )

  Recombination(
    SRH(DopingDependence TempDependence Tunneling(Hurkx))
    Auger
    Band2Band(Model=Hurkx)
    Avalanche(vanOverstraeten Eparallel)
  )
}

Plot {
  Doping DonorConcentration AcceptorConcentration
  eDensity hDensity SpaceCharge
  ElectricField/Vector Potential
  eQuasiFermi hQuasiFermi
  eGradQuasiFermi/Vector hGradQuasiFermi/Vector
  eCurrent/Vector hCurrent/Vector Current/Vector
  eMobility hMobility

  SRHRecombination Auger
  eBand2bandGeneration hBand2bandGeneration Band2bandGeneration
  eAvalancheGeneration hAvalancheGeneration AvalancheGeneration
  eAlphaAvalanche hAlphaAvalanche
  ConductionBandEnergy ValenceBandEnergy
}

CurrentPlot {
  Potential((0.0 0.0) (4.69 0.0) (12.50 0.0))
  ElectricField/Vector(
    (4.69 0.18) (4.69 0.26) (12.50 0.18) (12.50 0.26)
  )
  SRHRecombination(Integrate(Semiconductor))
  Band2bandGeneration(Integrate(Semiconductor))
  AvalancheGeneration(Integrate(Semiconductor))
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
  AvalDerivatives
  ExitOnFailure

  BreakCriteria {
    Current(Contact="anode" absval=1.0e-6)
  }
}

Solve {
  Coupled(Iterations=200 LineSearchDamping=1.0e-4) { Poisson }
  Coupled { Poisson Electron Hole }

  Quasistationary(
    InitialStep=1.0e-3
    MinStep=1.0e-9
    MaxStep=2.0e-3
    Increment=1.25
    Decrement=2.0
    Goal { Name="cathode" Voltage=@DARK_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
    CurrentPlot(Time=(Range=(0 1) Intervals=500))
  }
  Plot(FilePrefix="n@node@_DARK_NEAR")
}
