# -*- coding: utf-8 -*-
import psycopg2
from database.models import DATABASE_CONFIG

def clean_database():
    """Limpiar y reinicializar la base de datos"""
    try:
        # Conectar a la base de datos postgres por defecto
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database='postgres',
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            port=DATABASE_CONFIG['port']
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Desconectar usuarios y eliminar base de datos
        cur.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity 
            WHERE datname = '{DATABASE_CONFIG['database']}'
        """)
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_CONFIG['database']}")
        
        # Crear nueva base de datos con UTF-8
        cur.execute(f"""
            CREATE DATABASE {DATABASE_CONFIG['database']}
            WITH ENCODING 'UTF8'
            LC_COLLATE = 'Spanish_Spain.1252'
            LC_CTYPE = 'Spanish_Spain.1252'
            TEMPLATE template0;
        """)
        
        cur.close()
        conn.close()
        print("✅ Base de datos limpiada y reinicializada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al limpiar la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    clean_database()
