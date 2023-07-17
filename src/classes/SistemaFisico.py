import matplotlib.pyplot as plt
from GeradorDeDisturbios import GeradorDeDisturbios
from params import obter_parametros

class Misturador:
    entradas,saidas,dimensoes,setpoints,var_erro_zero,constantes_controlador = obter_parametros()
    def __init__(self,
                 entradas=entradas,
                 saidas=saidas,
                 dimensoes=dimensoes,
                 setpoints=setpoints,
                 var_erro_zero=var_erro_zero,
                 constantes_controlador=constantes_controlador) -> None:
        self.entradas = entradas
        self.saidas = saidas
        self.dimensoes = dimensoes
        self.setpoints = setpoints
        self.var_erro_zero = var_erro_zero
        self.constantes_controlador = constantes_controlador

    def listar_parametros(self):
        [F0,Fa0,Ca0] = self.entradas
        [F,Ca] = self.saidas
        [V] = self.dimensoes
        [Vset,Caset] = self.setpoints 
        [Ferrozero,F0errozero] = self.var_erro_zero
        [Kf,Tif,Tdf,KC,TiC,TdC] = self.constantes_controlador
        print(
        f"""
        Entradas:
            F0 = {F0} L/s       Fa0 = {Fa0} L/s     Ca0 = {Ca0} mol/L
        Saídas:
            F = {F} L/s         Ca = {Ca} L/s
        Dimensões:
            V = {V} L
        Setpoints:
            Vset = {Vset} L     Caset = {Caset} mol/L
        Variáveis no setpoint:
            F = {Ferrozero} L/s F0 = {F0errozero} L/s
        Constantes do controlador:
            Controlador de nível:
                Kc = {Kf}, Ti = {Tif}, Td = {Tdf}
            Controlador de concentração:
                Kc = {KC}, Ti = {TiC}, Td = {TdC}
        """
        )        

    def simular(self,
                disturbio: GeradorDeDisturbios,
                dt: float=0.005,
                tf: float=50,
                Rmax: float=0.1,
                tsample_inicial: float=1e-5):
        [F0,Fa0,Ca0] = self.entradas
        [F,Ca] = self.saidas
        [V] = self.dimensoes
        [Vset,Caset] = self.setpoints 
        [Ferrozero,F0errozero] = self.var_erro_zero
        [Kf,Tif,Tdf,KC,TiC,TdC] = self.constantes_controlador

        # Valores iniciais dos controladores
        intPIDV=0
        derPIDV=0
        erro1V=0
        erro2V=erro1V

        intPIDC=0
        derPIDC=0
        erro1C=0
        erro2C=erro1C

        Fant=F
        F0ant=F0

        # Calculando os produtos
        VCa = V*Ca

        def adaptar_sample(derivada):
            tsample=tsample_inicial  # Tempo de amostragem do controlador
            if derivada > 12 : # Derivada da vazao de entrada no tempo
                tsample=tsample_inicial/5

            elif derivada > 5 :
                tsample=tsample_inicial/2

            elif derivada > 2 :
                tsample=tsample_inicial
            return tsample
        
        # Inicio do loop
        tempo=0
        
        tempoV=[]
        VV=[]
        FV=[]  
        CaV=[]
        F0V=[]
        Fa0V=[]
        erro2VV=[]
        erro2CV=[]

        while (tempo<=tf):
            
            # Distúrbio
            Fa0 = disturbio.dist(tempo)

            tsampleF=adaptar_sample(abs(F-Fant)/dt)
            tsampleF0=adaptar_sample(abs(F0-F0ant)/dt)
            
            if (abs(round(tempo/tsampleF)  -  (tempo/tsampleF) )  < 1e-4):
                # Controlador PID no Volume
                #----------------------------------------------------------
                # A integral do PID no volume    
                intPIDV = intPIDV + (Vset-V)*dt
                # A derivada do PID no volume       
                derPIDV = (erro2V-erro1V)/dt
                erro1V = erro2V
                # A parte proporcional do PID no volume
                proPIDV = (Vset-V)
                # A equação do PID no volume
                F = Ferrozero + Kf*proPIDV + Kf*Tdf*derPIDV + (Kf/Tif)*intPIDV
                #----------------------------------------------------------   

            if (abs(round(tempo/tsampleF0)  -  (tempo/tsampleF0) )  < 1e-4):
                # Controlador PID na Concentração
                #----------------------------------------------------------
                # A integral do PID na Concentração    
                intPIDC = intPIDC + (Caset-Ca)*dt
                # A derivada do PID na Concentração       
                derPIDC = (erro2C-erro1C)/dt
                erro1C = erro2C
                # A parte proporcional do PID na Concentração
                proPIDC = (Caset-Ca)
                # A equação do PID na Concentração
                F0 = F0errozero + KC*proPIDC + KC*TdC*derPIDC + (KC/TiC)*intPIDC
                #----------------------------------------------------------   
            
            if (F >= Fant):
                if (F-Fant) > Rmax:
                    F = Fant + Rmax
            if (F < Fant):
                if (Fant - F) > Rmax:
                    F = Fant - Rmax
            Fant = F

            if (F0 >= F0ant):
                if (F0-F0ant) > Rmax:
                    F0 = F0ant + Rmax
            if (F0 < F0ant):
                if (F0ant - F0) > Rmax:
                    F0 = F0ant - Rmax
            F0ant = F0

            # Calculando as derivadas
            dVdt=F0+Fa0-F   
            dVCadt=Fa0*Ca0-F*Ca

            # Calculando as variaveis
            V=V+dVdt*dt                        
            VCa=VCa+dVCadt*dt
            Ca=VCa/V

            erro2V=Vset-V
            erro2C=Caset-Ca

            # Passo de tempo
            tempo = tempo + dt

            # Vetorizando
            tempoV.append(tempo)
            VV.append(V)
            FV.append(F)
            Fa0V.append(Fa0)
            F0V.append(F0)
            CaV.append(Ca)    
            erro2VV.append(erro2V**2)
            erro2CV.append(erro2C**2)

            self.vetores_para_plotagem = [tempoV,VV,FV,F0V,CaV,Fa0V]
            self.vetores_erro = [erro2VV,erro2CV]

        return self
    
    def plotar_graficos(self):

        [tempoV,VV,FV,F0V,CaV,Fa0V] = self.vetores_para_plotagem

        fig1, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3,2,sharex=True,sharey=False,figsize=(18,10))
        fig1.set_facecolor('white')

        ax1.plot(tempoV,VV)
        ax2.plot(tempoV,FV)
        ax3.plot(tempoV,CaV)
        ax4.plot(tempoV,F0V)
        ax5.plot(tempoV,Fa0V)

        ax1.set_ylabel("Volume do tanque")
        ax2.set_ylabel("Vazão de Saída")
        ax3.set_ylabel("Concentração")
        ax4.set_ylabel("Vazão de Diluente")
        ax5.set_ylabel("Vazão da esp. A (disturbio)")

        fig1.delaxes(ax6)

        plt.show()
    
    def score(self):
        assert hasattr(self,'vetores_erro')
        [erro2VV,erro2CV] = self.vetores_erro
        return (sum(erro2VV) + sum(erro2CV))/2
    
    def estado_estacionario(self):

        [Vset,Caset] = self.setpoints
        [F0,Fa0,Ca0] = self.entradas

        nulo = GeradorDeDisturbios(Vset).sinal_nulo()
        self.simular(nulo)

        [tempoV,VV,FV,F0V,CaV,Fa0V] = self.vetores_para_plotagem

        self.entradas = [F0V[-1],Fa0V[-1],Ca0]
        self.saidas = [FV[-1],CaV[-1]]
        self.dimensoes = [VV[-1]]
        self.var_erro_zero = [FV[-1],F0V[-1]]

        return self




