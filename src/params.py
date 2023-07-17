def obter_parametros():
    # ----------- Alimentacao (entrada) --------------
    F0=2.                         # litro/s
    Fa0=2.
    Ca0=1

    entradas = [F0,Fa0,Ca0]

    # ------------------- Saidas ----------------------
    F=4                            # litro/s
    Ca=0.5

    saidas = [F,Ca]

    # ------------------ Dimensoes -------------------
    V=10.                           # litros
    
    dimensoes = [V]
    
    # ------------------- Setpoints ---------------------
    Vset=10.                        # litros
    Caset=0.5

    setpoints = [Vset,Caset]
    
    # ----- Vazoes para quando o erro (variavel no setpoint - variavel) for zero ----
    Ferrozero = F                  # litros/2
    F0errozero = F0                  # litros/2

    var_erro_zero=[Ferrozero,F0errozero]

    # -------------------- Constantes do controlador --------------------------
    # Constantes do controlador da vazao de saida
    Kf=-5
    Tif=1
    Tdf=0

    # Constantes do controlador da vazao F0
    KC=-5
    TiC=0.1
    TdC=0

    constantes_controlador = [Kf,Tif,Tdf,KC,TiC,TdC]

    return entradas,saidas,dimensoes,setpoints,var_erro_zero,constantes_controlador