# -*- coding: utf-8 -*-
from database.models import init_database, User
import base64
import binascii

def check_admin():
    session = init_database()
    try:
        admin = session.query(User).filter_by(username="admin").first()
        if admin:
            print("\n=== Detalles del Usuario Admin ===")
            print(f"ID: {admin.id}")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Activo: {admin.is_active}")
            print("\n=== Detalles del Hash ===")
            print(f"Hash raw: {admin.password[:20]}...")
            print(f"Longitud del hash: {len(admin.password)}")
            
            # Intentar decodificar el hash
            try:
                # Intentar decodificar como base64
                decoded = base64.b64decode(admin.password)
                print("✅ Hash está en formato base64 válido")
                print(f"Longitud del hash decodificado: {len(decoded)} bytes")
                print(f"Primeros bytes del hash: {binascii.hexlify(decoded[:10]).decode()}")
            except Exception as e:
                print(f"❌ Error al decodificar hash: {str(e)}")
                # Si falla base64, mostrar como bytes directos
                try:
                    bytes_ver = admin.password.encode('utf-8')
                    print(f"Hash como bytes: {binascii.hexlify(bytes_ver[:10]).decode()}")
                except Exception as e2:
                    print(f"❌ Error al convertir a bytes: {str(e2)}")
        else:
            print("❌ Usuario admin no encontrado")
    finally:
        session.close()

if __name__ == "__main__":
    check_admin()
