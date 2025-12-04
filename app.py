#docker run -dti --name python-sql -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Senha@123" -e "MSSQL_PID=Express" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
#docker exec -it 3fa10032 /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P senha123
import pyodbc

print(pyodbc.drivers())


# Se conecta com o banco
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=master;UID=sa;PWD=Senha@123')

# Cria um cursor
cursor = cnxn.cursor()

# Lista todas as tabelas (usuário + sistema)
cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    ORDER BY TABLE_SCHEMA, TABLE_NAME
""")

tables = cursor.fetchall()

if not tables:
    print("Nenhuma tabela encontrada no banco.")
else:
    print("Tabelas encontradas:")
    for schema, table in tables:
        print(f"{schema}.{table}")

# Criando uma tabela
def criar_tabela(conexao, cursor, tabela):
    cursor.execute(f"CREATE TABLE {tabela} (" \
    'id int IDENTITY(1,1) PRIMARY KEY , ' \
    'nome VARCHAR(100), ' \
    'email VARCHAR(150),' \
    'CreatedAt DATE DEFAULT CURRENT_TIMESTAMP NOT NULL'\
    ')')
    # Comitar para 'salvar' o que foi feito
    conexao.commit()

#criar_tabela(cnxn, cursor, 'clientes')

#data = ('Thiago', 'thiagodebia@gmail.com')

def inserir_registro(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?,?)', data)
    conexao.commit()

def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?;', data)
    conexao.commit()

#atualizar_registro(cnxn, cursor, "Thiago Debia", 'thiago@hotmail.com', 1)

def deletar_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?;', data)
    conexao.commit()

#deletar_registro(cnxn, cursor,1)

def inserir_muitos(conexao, cursor, dados):
    cursor.executemany('INSERT INTO clientes (nome, email) VALUES (?,?)', dados)
    conexao.commit()

dados=[
    ('Thiago','thiago@gmail.com'),
    ('Juliana','juliana@gmail.com'),
    ('Arthur','arthur@gmail.com')
]

#inserir_muitos(cnxn, cursor, dados)
    
def listar_clientes(cursor, tabela):
    cursor.execute(f'SELECT * FROM {tabela} ORDER BY nome')
    results = cursor.fetchall()
    for row in results:
        print(row)

listar_clientes(cursor,'clientes')

def listar_cliente_por_id(cursor, id):
    cursor.execute(f'SELECT * FROM clientes WHERE id=?', (id,))
    return cursor.fetchone()
    

print(listar_cliente_por_id(cursor,2))