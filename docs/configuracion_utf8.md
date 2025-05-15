# Configuración de Codificación UTF-8

## Configuración de Base de Datos

La aplicación utiliza las siguientes configuraciones para asegurar el correcto manejo de caracteres especiales:

### Parámetros de Conexión
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'integral_service_db',
    'user': 'postgres',
    'password': '****',
    'port': '5432',
    'client_encoding': 'utf8',
    'options': '-c client_encoding=utf8'
}
```

### Configuración del Motor SQLAlchemy
```python
engine = create_engine(
    db_url, 
    echo=False,
    connect_args={
        'client_encoding': 'utf8',
        'options': '-c search_path=public -c client_encoding=utf8'
    }
)
```

## Verificación de Codificación

Para verificar la configuración de codificación:
1. Ejecutar `python database/check_encoding.py`
2. Verificar que tanto el servidor como el cliente muestren UTF8

## Plan de Rollback

En caso de problemas con la codificación:

1. Backup de Datos:
   ```bash
   python database/backup_db.py
   ```

2. Revertir a Configuración Anterior:
   - Restaurar configuración previa de DATABASE_CONFIG
   - Ejecutar `python database/init_tables.py`
   - Restaurar datos desde el backup

3. Verificación Post-Rollback:
   ```bash
   python database/verify_db.py
   ```

## Pruebas de Caracteres Especiales

Para verificar el correcto funcionamiento:

1. Insertar datos con caracteres especiales
2. Verificar la correcta visualización
3. Validar en todas las interfaces (CLI, Web, PDF)

## Mantenimiento

- Ejecutar verificaciones periódicas de codificación
- Mantener backups actualizados
- Monitorear logs por errores de codificación
