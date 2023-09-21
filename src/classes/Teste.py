import sqlite3

con = sqlite3.connect('teste.db')
cur = con.cursor() 

cur.execute(""" Create Table if not exists IndIntConst (Tipo_do_disturbio, Intensidade_do_disturbio, Erro, Kf, Tif, Tdf, Kc, Tic, Tdc) """)

Tipo = 'jorge'
Int = 1
Erro = 8
Kf = 1
Tif = 2
Tdf = 3
Kc = 4
Tic = 5
Tdc = 6

Erro_novo = 5

# Inserindo os valores
#cur.execute(""" Insert into IndIntConst Values (?, ?, ?, ?, ?, ?, ?, ?, ?)""",(Tipo,Int,Erro,Kf,Tif,Tdf,Kc,Tic,Tdc))

# Comparando erros
# cur.execute("""UPDATE IndIntConst SET Erro = CASE WHEN ? < Erro THEN ? ELSE Erro END WHERE Tipo_do_disturbio = ? """, (Erro_novo,Erro_novo,Tipo))

# cur.execute("""UPDATE IndIntConst SET Erro = CASE WHEN ? < Erro THEN ? ELSE Erro END WHERE Tipo_do_disturbio = ? """, (Erro_novo,Erro_novo,Tipo))

cur.execute(""" SELECT Erro FROM IndIntConst WHERE tipo_do_disturbio = ? AND Intensidade_do_disturbio = ?""",(Tipo, Int))
erro_atual = cur.fetchone()
print(erro_atual[0])


# Confirmando as mudanças
con.commit()

# Fechando o banco de dados meuBanco
con.close()

