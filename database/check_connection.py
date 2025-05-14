# -*- coding: utf-8 -*-
import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse, parse_qs
import sys

# Configurar la codificación por defecto
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def check_postgres():
    """Verificar la conexión a PostgreSQL"""
    load_dotenv()
    
    # Obtener configuración de la base de datos
    db_url = os.getenv('DATABASE_URL', '').strip()
    if not db_url:
        print("ERROR: No se encontró DATABASE_URL en las variables de entorno")
        return False
    
    try:
        # Parsear la URL de la base de datos de forma segura
        parsed = urlparse(db_url)
        query_params = parse_qs(parsed.query)
        
        # Extraer los componentes
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        port = parsed.port or 5432
        dbname = parsed.path.lstrip('/')
        
        # Extraer parámetros adicionales
        client_encoding = query_params.get('client_encoding', ['UTF8'])[0]
        
        if not all([user, password, host]):
            print("ERROR: URL de base de datos malformada. Formato esperado:")
            print("postgresql://usuario:contraseña@host:puerto/nombre_db")
            return False
        
        # Intentar conectar al servidor PostgreSQL
        print("Intentando conectar al servidor PostgreSQL...")
        conn = psycopg2.connect(
            user='postgres',
            password='DAms15820',
            host='localhost',
            port='5432',
            client_encoding=client_encoding
        )
        conn.close()
        print("✓ Conexión al servidor PostgreSQL exitosa")
        
        # Intentar conectar a la base de datos específica
        print(f"Intentando conectar a la base de datos {dbname}...")
        try:
            conn = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=dbname,
                client_encoding=client_encoding
            )
            conn.close()
            print(f"✓ Conexión a la base de datos {dbname} exitosa")
            return True
        except psycopg2.OperationalError as e:
            if "does not exist" in str(e):
                print(f"La base de datos {dbname} no existe. Intentando crearla...")
                try:
                    # Conectar a la base de datos por defecto para crear la nueva
                    conn = psycopg2.connect(
                        user=user,
                        password=password,
                        host=host,
                        port=port,
                        database='postgres',
                        client_encoding=client_encoding
                    )
                    conn.autocommit = True
                    cur = conn.cursor()
                    
                    # Crear la base de datos con codificación UTF-8
                    cur.execute(f"CREATE DATABASE {dbname} ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0")
                    cur.close()
                    conn.close()
                    print(f"✓ Base de datos {dbname} creada exitosamente")
                    return True
                except Exception as create_error:
                    print(f"Error al crear la base de datos: {str(create_error)}")
                    return False
            else:
                print(f"Error de conexión: {str(e)}")
                return False
                
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que PostgreSQL esté instalado y en ejecución")
        print("2. Verifica que el usuario y contraseña sean correctos")
        print("3. Verifica que el puerto sea correcto (por defecto 5432)")
        print("4. Verifica que el servidor esté aceptando conexiones")
        return False

if __name__ == "__main__":
    check_postgres()
