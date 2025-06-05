import psycopg2

def executar_sql_arquivo(cursor, caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        sql = f.read()
    cursor.execute(sql)

def main():
    conn = psycopg2.connect(
        host="localhost",
        dbname="smartpark",
        user="postgres",
        password="admin",
        port=5432
    )

    try:
        cursor = conn.cursor()

        arquivos_populate = [
            'populate_usuario.sql',
            # 'populate_evento.sql',
            # 'populate_outro.sql',
        ]

        for arquivo in arquivos_populate:
            print(f"Executando {arquivo}...")
            executar_sql_arquivo(cursor, arquivo)

        conn.commit()
        print("População concluída com sucesso!")

    except Exception as e:
        conn.rollback()
        print("Erro ao popular o banco:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
