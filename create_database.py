import sqlite3

def cria_db():
    connection = sqlite3.connect('adivinhacao_ranking.db')
    create = connection.cursor()
    create.execute('''CREATE TABLE RANKING ([Nome] text, [Pontuacao] integer)''')
    connection.commit()
    create.close()