#setdep @node|-1@
#setdep @node|-3@

* CMP SPAD SDevice2
* Multi-bias SCR / ATP diagnostics
* Avalanche feedback OFF
* No embedded Tcl preprocessing blocks
*
* Parent -1: SVisualPy1
* Parent -3: SNMesh2
*
* SProcess interface: raw_y = 0.300 um

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

  EffectiveIntrinsicDensity(
    OldSlotboom
  )

  Mobility(
    DopingDependence
    HighFieldSaturation(GradQuasiFermi)
    Enormal
  )

  Recombination(
    SRH(
      DopingDependence
      TempDependence
      Tunneling(Hurkx)
    )

    Auger

    Band2Band(
      Model=Hurkx
    )

    Avalanche(
      vanOverstraeten ElectricField
    )
  )

  BreakdownProbability(
    MinElectricField=1.0e5
    InterpolatedDiscretization
  )
}

Plot {

  Doping
  DonorConcentration
  AcceptorConcentration

  eDensity
  hDensity
  SpaceCharge

  ElectricField/Vector
  Potential

  eQuasiFermi
  hQuasiFermi

  eGradQuasiFermi/Vector
  hGradQuasiFermi/Vector

  eCurrent/Vector
  hCurrent/Vector
  Current/Vector

  eMobility
  hMobility

  SRHRecombination
  Auger

  eBand2bandGeneration
  hBand2bandGeneration
  Band2bandGeneration

  eAvalancheGeneration
  hAvalancheGeneration
  AvalancheGeneration

  eAlphaAvalanche
  hAlphaAvalanche

  eIonIntegral
  hIonIntegral
  MeanIonIntegral

  eBreakdownProbability
  hBreakdownProbability
  jBreakdownProbability

  ConductionBandEnergy
  ValenceBandEnergy
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

  Number_of_Threads=64

  RhsMin=1.0e-15

  ExitOnFailure

  SaveWithinMinStep

  AvalPostProcessing

  ComputeIonizationIntegrals(
    MinElectricField=2.0e5
    SaveEIonIntegralPaths=1
    SaveHIonIntegralPaths=1
    WriteAll
  )
}

Solve {

  Coupled(
    Iterations=200
    LineSearchDamping=1.0e-4
  ){
    Poisson
  }

  Coupled {
    Poisson Electron Hole
  }

  * Single monotonic voltage ramp.
  * All snapshot times are extracted by SVisualPy1.

  Quasistationary(

    InitialStep=1.0e-3
    MinStep=1.0e-9
    MaxStep=2.0e-3

    Increment=1.25
    Decrement=2.0

    Goal {
      Name="cathode"
      Voltage=@SD2_END_V@
    }

  ){

    Coupled {
      Poisson Electron Hole
    }

    * Original SCR evaluation bias

    Plot(
      FilePrefix="n@node@_SCR"
      Time=(@SD2_T_SCR@)
    )

    * Fixed absolute bias: 15.0 V

    Plot(
      FilePrefix="n@node@_V150"
      Time=(@SD2_T_V150@)
    )

    * Diagnostic reference VBD

    Plot(
      FilePrefix="n@node@_VBD"
      Time=(@SD2_T_VBD@)
    )

    * VBD + 0.5 V

    Plot(
      FilePrefix="n@node@_VEX05"
      Time=(@SD2_T_VEX05@)
    )

    * VBD + 1.0 V

    Plot(
      FilePrefix="n@node@_VEX10"
      Time=(@SD2_T_VEX10@)
    )

    * Original ATP evaluation bias

    Plot(
      FilePrefix="n@node@_ATP"
      Time=(@SD2_T_ATP@)
    )

    * VBD + 1.5 V

    Plot(
      FilePrefix="n@node@_VEX15"
      Time=(@SD2_T_VEX15@)
    )

  }
}
