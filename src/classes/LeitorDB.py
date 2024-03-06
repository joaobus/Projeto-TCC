import sqlite3
import numpy as np

class LeitorDB:


    def Leitor(self,intensidade):
        con = sqlite3.connect('banco_constantes.db')
        cur = con.cursor() 

        tipo = "degrau"

        sqlquery = ("""SELECT Kf, Tif, Tdf, Kc, Tic, Tdc FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio = ?""")
        cur.execute(sqlquery,(tipo, intensidade))
        constantes = (cur.fetchone())

        if(cur.fetchone() is None):
            sqlqueryUP = ("""SELECT Kf, Tif, Tdf, Kc, Tic, Tdc FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio > ? ORDER BY Intensidade_do_disturbio LIMIT 1""")
            cur.execute(sqlqueryUP,(tipo, intensidade))
            ListaUP = (cur.fetchone())

            sqlqueryINT_UP = ("""SELECT Intensidade_do_disturbio FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio > ? ORDER BY Intensidade_do_disturbio LIMIT 1""")
            cur.execute(sqlqueryINT_UP,(tipo, intensidade))
            intensidade_UP = (cur.fetchone())
            
            sqlqueryDOWN = ("""SELECT Kf, Tif, Tdf, Kc, Tic, Tdc FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio < ? ORDER BY Intensidade_do_disturbio DESC LIMIT 1""")
            cur.execute(sqlqueryDOWN,(tipo, intensidade))
            ListaDOWN=(cur.fetchone())

            sqlqueryINT_DOWN = ("""SELECT Intensidade_do_disturbio FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio < ? ORDER BY Intensidade_do_disturbio DESC LIMIT 1""")
            cur.execute(sqlqueryINT_DOWN,(tipo, intensidade))
            intensidade_DOWN = (cur.fetchone())
        
            
        def interpolate(ListaDOWN, ListaUP, intensidade,intensidade_DOWN,intensidade_UP):
            return [(ListaDOWN[i]+(ListaUP[i]-ListaDOWN[i])*((intensidade - intensidade_DOWN[0])/(intensidade_UP[0]-intensidade_DOWN[0]))) for i in range (len(ListaUP))]

        constantes = interpolate(ListaDOWN,ListaUP,intensidade,intensidade_DOWN,intensidade_UP)
        return constantes
        

