import numpy as np

class GeradorDeDisturbios:
    def __init__(self,varset):
        self.varset = varset

    def degrau(self,intensidade,inicio=0):
        self.tipo = "degrau"
        self.intensidade = intensidade
        self.dist = lambda t: self.varset + self.varset*intensidade if t>=inicio else self.varset
        return self 

    def pulso(self,intensidade,inicio=0,fim=100):
        self.tipo = "pulso"
        self.intensidade = intensidade
        self.dist = lambda t: self.varset + self.varset*intensidade if inicio<=t<=fim else self.varset
        return self

    def rampa(self,inclinacao,inicio=0):
        self.tipo = "rampa"
        self.intensidade = inclinacao
        self.dist = lambda t: inclinacao*(t-inicio) + self.varset if t>=inicio else self.varset
        return self

    def senoidal(self,amplitude,frequencia,inicio=0):
        self.tipo = "senoidal"
        self.intensidade = amplitude
        self.dist = lambda t: amplitude*self.varset*np.sin(frequencia*(t-inicio)) + self.varset if t>=inicio else self.varset
        return self
    
    def sinal_composto(self,disturbios_a_somar):
        n = len(disturbios_a_somar)
        self.tipo = "composto"
        self.intensidade = None
        self.dist = lambda t: sum([disturbio.dist(t) for disturbio in disturbios_a_somar]) - (n-1)*self.varset
        return self
    
    def sinal_nulo(self):
        self.tipo = "nulo"
        self.intensidade = None
        self.dist = lambda t: self.varset
        return self