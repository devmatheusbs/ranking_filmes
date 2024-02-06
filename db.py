import sqlite3
def criardb():
    try:
        con = sqlite3.connect('filmesdb.db')        
    except sqlite3.Error as e: 
        print(' O banco de dados não está acessível')
    try:
        with con:
            cur = con.cursor()
            cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS Filmes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title VARCHAR(100) NOT NULL,
                        year DATE,
                        runtime VARCHAR(12),
                        director TEXT,
                        writer TEXT,
                        genre TEXT,
                        actors TEXT,
                        plot TEXT,
                        imdbrating FLOAT,
                        userrating FLOAT            
                     )
                """)
                    
    except sqlite3.Error as e:
        print('Erro ao criar a tabela de filmes', e)
    finally:
        con.close()

def inserir_filme(title, year, runtime, director, writer, genre, actors, plot, imdbrating, userrating):
    conexao = sqlite3.connect('filmesdb.db')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO Filmes (title, year, runtime, director, writer, genre, actors, plot, imdbrating, userrating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, year, runtime, director, writer, genre, actors, plot, imdbrating, userrating))
    conexao.commit()
    conexao.close()

def selecionar_filmes():
    conexao = sqlite3.connect('filmesdb.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Filmes')
    filmes = cursor.fetchall()
    conexao.close()
    return filmes

def atualizar_filme(id, title, year, runtime, director, writer, genre, actors, plot, imdbrating, userrating):
    conexao = sqlite3.connect('filmesdb.db')
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE Filmes SET title=?, year=?, runtime=?, director=?, writer=?, genre=?, actors=?, plot=?, imdbrating=?, userrating=?
        WHERE id=?
    ''', (title, year, runtime, director, writer, genre, actors, plot, imdbrating, userrating, id))
    conexao.commit()
    conexao.close()

def excluir_filme(id):
    conexao = sqlite3.connect('filmesdb.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM Filmes WHERE id=?', (id,))
    conexao.commit()
    conexao.close()


