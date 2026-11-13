#setdep @node|-1@
#setdep @node|-3@

* CMP SPAD SDevice2 - percent-of-VBD SCR and ATP at extracted biases
* 2026-08-28
* Parent -1 is SVisualPy1; parent -3 is SNMesh2 (mesh source).
* The SV1 DOE variables replace the goals for each experiment.
* Exact goal-state TDRs: n<node>_SCR_des.tdr and n<node>_ATP_des.tdr.
* Diagnostic physics/solver copied from prior SDE ATP diagnostic deck.
* CAUTION: Avalanche ElectricField differs from SDevice1 GradQuasiFermi VBD.
* This is a convergence experiment, NOT yet a harmonized final VBD/ATP model.
* BreakAtIonIntegral is intentionally absent so ATP can be evaluated.
* SProcess interface coordinate: z_if = raw_y - 0.300 um.

File {
  Grid    = "n@node|-3@_msh.tdr"
  Current = "@plot@"
  Plot    = "@tdrdat@"
  Output  = "@log@"
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
  }
  * Final converged state at SCR_BIAS_V = VBD*(1-SCR_BELOW_VBD_PCT/100).
  Plot(FilePrefix="n@node@_SCR")
  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-3
    Increment=1.25 Decrement=2.0
    Goal { Name="cathode" Voltage=@ATP_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
  }
  * Final converged state at ATP_BIAS_V = VBD*(1+ATP_ABOVE_VBD_PCT/100).
  Plot(FilePrefix="n@node@_ATP")
}
