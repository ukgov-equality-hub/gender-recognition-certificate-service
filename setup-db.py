import psycopg2


conn = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='password',
    host='localhost',
    port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('CREATE database grc')
print('Database created successfully...')
conn.close()
