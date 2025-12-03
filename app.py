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
cursor.execute('CREATE TABLE clientes (' \
'id int IDENTITY(1,1) PRIMARY KEY , ' \
'nome VARCHAR(100), ' \
'email VARCHAR(150),' \
'CreatedAt DATE DEFAULT CURRENT_TIMESTAMP NOT NULL'\
')')

#cursor.execute('INSERT INTO clientes (id, nome, email) VALUES (1, "Thiago","thiagodebia@gmail.com")')

#cursor.execute('SELECT * FROM clientes')