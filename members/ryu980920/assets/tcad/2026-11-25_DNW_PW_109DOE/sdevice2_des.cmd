#setdep @node|-1@
#setdep @node|-3@
#setdep @node|-5@

* CMP SPAD SDevice3
* Multi-bias Dark Current diagnostics
* Avalanche feedback ON
* No embedded Tcl preprocessing blocks
*
* Parent -1: SVisualPy2
* Parent -3: SVisualPy1
* Parent -5: SNMesh2
*
* SProcess interface: raw_y = 0.300 um

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
      vanOverstraeten Eparallel
    )

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

  ConductionBandEnergy
  ValenceBandEnergy
}

CurrentPlot {

  Potential(
    (0.0 0.0)
    (4.69 0.0)
    (12.50 0.0)
  )

  ElectricField/Vector(
    (4.69 0.18)
    (4.69 0.26)
    (12.50 0.18)
    (12.50 0.26)
  )

  SRHRecombination(
    Integrate(Semiconductor)
  )

  Band2bandGeneration(
    Integrate(Semiconductor)
  )

  AvalancheGeneration(
    Integrate(Semiconductor)
  )
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

  AvalDerivatives

  ExitOnFailure

  SaveWithinMinStep

  BreakCriteria {

    Current(
      Contact="anode"
      absval=1.0e-6
    )

  }
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

  * Equilibrium state

  Plot(
    FilePrefix="n@node@_V000"
  )

  * Original dark-current voltage ramp

  Quasistationary(

    InitialStep=1.0e-3
    MinStep=1.0e-9
    MaxStep=2.0e-3

    Increment=1.25
    Decrement=2.0

    Goal {
      Name="cathode"
      Voltage=@DARK_BIAS_V@
    }

  ){

    Coupled {
      Poisson Electron Hole
    }

    CurrentPlot(
      Time=(
        Range=(0 1)
        Intervals=500
      )
    )

    * 50 percent of VBD

    Plot(
      FilePrefix="n@node@_BD50"
      Time=(@SD3_T_BD50@)
    )

    * Fixed absolute bias: 12 V

    Plot(
      FilePrefix="n@node@_V120"
      When(
        Contact="cathode"
        Voltage=12.0
      )
    )

    * Fixed absolute bias: 13 V

    Plot(
      FilePrefix="n@node@_V130"
      When(
        Contact="cathode"
        Voltage=13.0
      )
    )

    * Fixed absolute bias: 14 V

    Plot(
      FilePrefix="n@node@_V140"
      When(
        Contact="cathode"
        Voltage=14.0
      )
    )

    * 90 percent of VBD

    Plot(
      FilePrefix="n@node@_BD90"
      Time=(@SD3_T_BD90@)
    )

    * 95 percent of VBD

    Plot(
      FilePrefix="n@node@_BD95"
      Time=(@SD3_T_BD95@)
    )

    * Original DARK_BIAS_V state

    Plot(
      FilePrefix="n@node@_DARK_NEAR"
      Time=(1.0)
    )

  }
}
