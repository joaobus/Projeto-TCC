import sqlite3

con = sqlite3.connect('banco_constantes.db')
cur = con.cursor() 

intensidade = 0.1
tipo = "degrau"

sqlquery = ("""SELECT Kf, Tif, Tdf, Kc, Tic, Tdc FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio = ?""")
cur.execute(sqlquery,(tipo, intensidade))
print(cur.fetchone())
