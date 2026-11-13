#setdep @node|-1@
#setdep @node|-3@

* H2 SDevice2 - dynamic SCR/PEB/ATP with SDE ATP-baseline physics aligned
* Physics and ionization controls: CMP_SPAD_Diagnostic_ATP_SDevice.txt
* H2-specific -1 SV1 dependency, -3 SNMesh2 dependency and dynamic biases retained.
* Diagnostic feedback OFF. Do not use BreakAtIonIntegral, as ATP is above VBD.
* NOTE: this ATP avalanche driving force (ElectricField) intentionally differs
* from SDevice1 VBD (GradQuasiFermi), as in the original SDE baseline decks.
* Exact goal-state TDRs: n<node>_SCR_des.tdr, _PEB_des.tdr, _ATP_des.tdr.

File {
  Grid        = "n@node|-3@_msh.tdr"
  Current     = "@plot@"
  Plot        = "@tdrdat@"
  Output      = "@log@"
  IonIntegral = "n@node@_ionpath.tdr"
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
    Avalanche(vanOverstraeten ElectricField)
  )

  BreakdownProbability(
    MinElectricField=1.0e5
    InterpolatedDiscretization
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
  eIonIntegral hIonIntegral MeanIonIntegral
  eBreakdownProbability hBreakdownProbability jBreakdownProbability
  ConductionBandEnergy ValenceBandEnergy
}

* Integrated generation quantities are diagnostics only in this feedback-OFF deck.
CurrentPlot {
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
  Iterations=100
  Notdamped=100
  Number_of_Threads=4
  RhsMin=1.0e-15
  ExitOnFailure

  AvalPostProcessing

  ComputeIonizationIntegrals(
    MinElectricField=2.0e5
    SaveEIonIntegralPaths=1
    SaveHIonIntegralPaths=1
    WriteAll
  )
}

Solve {
  Coupled(Iterations=200 LineSearchDamping=1.0e-4) { Poisson }
  Coupled { Poisson Electron Hole }

  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-3
    Increment=1.25 Decrement=2.0
    Goal { Name="cathode" Voltage=@SCR_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
    CurrentPlot(Time=(Range=(0 1) Intervals=500))
  }
  Plot(FilePrefix="n@node@_SCR")

  * Separate near-breakdown field/PEB diagnostic (0.999 * VBD).
  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-3
    Increment=1.25 Decrement=2.0
    Goal { Name="cathode" Voltage=@PEB_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
    CurrentPlot(Time=(Range=(0 1) Intervals=500))
  }
  Plot(FilePrefix="n@node@_PEB")

  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-3
    Increment=1.25 Decrement=2.0
    Goal { Name="cathode" Voltage=@ATP_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
    CurrentPlot(Time=(Range=(0 1) Intervals=500))
  }
  Plot(FilePrefix="n@node@_ATP")
}
