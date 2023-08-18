import sqlite3
from skopt import gp_minimize

#comment

from classes.SistemaFisico import Misturador
from classes.GeradorDeDisturbios import GeradorDeDisturbios

class AnalisadorDeConstantes:
    def __init__(self,
                 sistema_fisico,
                 Rmax: float,
                 tsample_inicial: float,
                 disturbio: GeradorDeDisturbios):
        self.sistema_fisico = sistema_fisico
        self.rmax = Rmax
        self.tsample_inicial = tsample_inicial
        self.disturbio = disturbio
    
    def otimizar_constantes(self):
        
        def erro(constantes_controlador):
            self.sistema_fisico.constantes_controlador = constantes_controlador
            self.sistema_fisico.simular(Rmax=self.rmax,
                                              tsample_inicial=self.tsample_inicial,
                                              disturbio=self.disturbio)
            return self.sistema_fisico.score()

        # Define os limites para os parâmetros Kc, Ti e Td para cada controlador
        pid1_range = [(-50, -0.01),(0.01, 5),(0, 0.01)]
        pid2_range = [(-50, -0.01),(0.01, 5),(0, 0.01)]

        dims = pid1_range + pid2_range

        resultado = gp_minimize(erro,dims,n_calls=30)
        self.melhores_constantes = resultado.x            # type:ignore
        return self

    def escrever_no_banco(self):

        [Kf,Tif,Tdf,Kc,Tic,Tdc] = self.melhores_constantes
        
        con = sqlite3.connect('banco_constantes.db')
        cur = con.cursor() 

        # Criando a tabela
        cur.execute(""" Create Table if not exists IndIntConst (Tipo_do_disturbio, Intensidade_do_disturbio, Kf, Tif, Tdf, Kc, Tic, Tdc) """)

        # Inserindo os valores
        cur.execute(""" Insert into IndIntConst Values (?, ?, ?, ?, ?, ?, ?, ?)""",(self.disturbio.tipo,
                                                                                    self.disturbio.intensidade,
                                                                                    Kf,Tif,Tdf,Kc,Tic,Tdc))

        # Confirmando as mudanças
        con.commit()

        # Fechando o banco de dados meuBanco
        con.close()
