import random
import sqlite3
import pandas as pd
import create_database
import os.path

def check_if_db_was_created_before():
    if os.path.isfile('adivinhacao_ranking.db'):
        return True
    else:
        return False
def jogar():
    while check_if_db_was_created_before() == False:
        create_database.cria_db()

    print("*********************************")
    print("Bem vindo no jogo de Adivinhação!")
    print("*********************************")

    numero_secreto = random.randrange(1, 101)
    total_de_tentativas = 0
    pontos = 1000

    connection = sqlite3.connect('adivinhacao_ranking.db')
    create = connection.cursor()

    print("Qual nível de dificuldade você quer?")
    print("(1) Fácil - (2) Médio - (3) Difícil")

    nivel = int(input("Define o nível: "))

    if(nivel == 1):
        total_de_tentativas = 20
    elif(nivel == 2):
        total_de_tentativas = 10
    elif(nivel == 3):
        total_de_tentativas = 5
    else:
        print("\nVocê precisa digitar 1, 2 ou 3 para funcionar.")

    for rodada in range(1, total_de_tentativas + 1):
        print(f"Tentativa {rodada} de {total_de_tentativas}!")
        chute_str = input("Digite um número entre 1 e 100: ")
        if(not chute_str.isdigit()):
            print("Você deve digitar um número entre 1 e 100! Letras e outros símbolos não são aceitos.")
            continue
        print("Você digitou: ", chute_str)
        chute = int(chute_str)

        if(chute < 1 or chute > 100):
            print("Você deve digitar um número entre 1 e 100!")
            continue
        acertou = chute == numero_secreto
        maior   = chute >  numero_secreto
        menor   = chute <  numero_secreto

        if(acertou):
            pontuaçao_final = pontos * 10 * nivel if rodada == 1 else pontos / rodada * nivel
            print(f"Você acertou e fez {pontuaçao_final:05.0f} pontos!")
            nome = input("Se quiser salvar sua pontuação digite seu nome, se não aperte \"enter\": ")
            if len(nome) == 0:
                break
            else:
                connection.execute("INSERT INTO RANKING VALUES (?,?)", (nome, pontuaçao_final))
            break
        elif(menor):
            print("Você errou! Seu chute foi menor que o numero secreto!")
        elif(maior):
            print("Você errou! Seu chute foi maior que o numero secreto!")
        pontos_perdidos = abs(numero_secreto - chute)
        pontos -= pontos_perdidos

    print("Fim do jogo! \n Ranking:")
    create.execute("select * from RANKING")
    connection.commit()
    df = pd.DataFrame(create.fetchall(), columns=['Nome','Pontuacao'])
    print(df.sort_values(by='Pontuacao', ascending=False).to_string(index=False))
    create.close()

if(__name__ == "__main__"):
    jogar()
