import sqlite3
from skopt import gp_minimize

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
            return self.sistema_fisico.erro()

        # Define os limites para os parâmetros Kc, Ti e Td para cada controlador
        pid1_range = [(-50, -0.01),(0.01, 5),(0, 0.01)]
        pid2_range = [(-50, -0.01),(0.01, 5),(0, 0.01)]

        dims = pid1_range + pid2_range

        resultado = gp_minimize(erro,dims,n_calls=70)
        self.melhores_constantes = resultado.x            # type:ignore
        return self

    def escrever_no_banco(self):

        [Kf,Tif,Tdf,Kc,Tic,Tdc] = self.melhores_constantes
        self.sistema_fisico.constantes_controlador = self.melhores_constantes
        self.sistema_fisico.simular(self.disturbio)
        erro = self.sistema_fisico.erro()


        con = sqlite3.connect('banco_constantes.db')
        cur = con.cursor() 

        # Criando a tabela
        cur.execute(""" Create Table if not exists IndIntConst (Tipo_do_disturbio, Intensidade_do_disturbio, Erro, Kf, Tif, Tdf, Kc, Tic, Tdc) """)

        cur.execute(""" SELECT Erro FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio = ?""",(self.disturbio.tipo, self.disturbio.intensidade))
        erro_atual = cur.fetchone()
        print(erro)

        if erro_atual is None: 
            # Inserindo os valores
            cur.execute(""" Insert into IndIntConst Values (?, ?, ?, ?, ?, ?, ?, ?, ?)""",(self.disturbio.tipo,
                                                                                        self.disturbio.intensidade,
                                                                                        self.sistema_fisico.erro(),
                                                                                        Kf,Tif,Tdf,Kc,Tic,Tdc))
        # Atualizar valores com erro menor                                                                                
        elif erro < erro_atual[0]:
            cur.execute("""UPDATE IndIntConst SET Erro = ?, Kf = ?, Tif = ?, Tdf = ?, Kc = ?, Tic = ?, Tdc = ? WHERE Tipo_do_disturbio = ? AND Intensidade_do_disturbio = ? """, 
            (erro,Kf,Tif,Tdf,Kc,Tic,Tdc,self.disturbio.tipo, self.disturbio.intensidade))


        # Confirmando as mudanças
        con.commit()

        # Fechando o banco de dados meuBanco
        con.close()
