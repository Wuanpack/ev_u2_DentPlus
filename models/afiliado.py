"""Model para realizar peticiones a la BBDD"""
import sqlite3
import re

DB_PATH = 'dentplus.db'

def get_connection():
    """Obtiene la conexión con la Base de Datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicia la conexión con la base de datos y crea la tabla afiliados si no existe"""
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS afiliados (
                afiliado_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                membership_type TEXT NOT NULL CHECK(membership_type IN ('silver', 'gold', 'platinum')),
                estado INTEGER NOT NULL DEFAULT 1
                )
        ''')

def get_all(search=None, membership_type=None):
    """Obtiene todos los afiliados ACTIVOS (estado = 1) con búsqueda y filtros adicionales"""
    query = 'SELECT * FROM afiliados WHERE estado = 1'
    params = []

    if search:
        query += ' AND (first_name LIKE ? OR last_name LIKE ? OR email LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

    if membership_type:
        query += ' AND membership_type = ?'
        params.append(membership_type)

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()

def get_all_inactive():
    """Obtiene todos los afiliados INACTIVOS (estado = 0)"""
    with get_connection() as conn:
        return conn.execute('SELECT * FROM afiliados WHERE estado = 0').fetchall()

def get_by_id(afiliado_id):
    """Obtiene los datos de un afiliado dependiendo de su afiliado_id"""
    with get_connection() as conn:
        return conn.execute('SELECT * FROM afiliados WHERE afiliado_id = ?', (afiliado_id,)).fetchone()

def create(first_name, last_name, email, membership_type):
    """Crea un afiliado tomando como inputs el first_name, last_name, email y membership_type"""
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO afiliados (first_name, last_name, email, membership_type) VALUES (?,?,?,?)',
            (first_name, last_name, email, membership_type)
        )

def update(afiliado_id, first_name, last_name, email, membership_type):
    """Modifica los datos de un usuario (first_name, last_name, email, membership_type) dependiendo de su afiliado_id"""
    with get_connection() as conn:
        conn.execute(
            'UPDATE afiliados SET first_name=?, last_name=?, email=?, membership_type=? WHERE afiliado_id=?',
            (first_name, last_name, email, membership_type, afiliado_id)
        )

def deactivate(afiliado_id):
    """Desactiva un usuario dependiendo de su afiliado_id"""
    with get_connection() as conn:
        conn.execute('UPDATE afiliados SET estado = 0 WHERE afiliado_id=?', (afiliado_id,))

def activate(afiliado_id):
    """Reactiva un usuario dependiendo de su afiliado_id"""
    with get_connection() as conn:
        conn.execute('UPDATE afiliados SET estado = 1 WHERE afiliado_id=?', (afiliado_id,))

def calcular_descuento(membership_type, monto):
    """Calcula el descuento de un monto dependiendo del membershipType"""
    descuentos = {
        'silver': 0.05,
        'gold': 0.10,
        'platinum': 0.20
    }
    porcentaje = descuentos.get(membership_type, 0)
    descuento = monto * porcentaje
    total = monto - descuento
    return round(descuento, 2), round(total, 2)

def validar_afiliado(first_name, last_name, email, membership_type):
    """Valida los datos de un afiliado y retorna una lista de errores"""
    errors = []

    if not first_name or len(first_name.strip()) < 2:
        errors.append('El nombre debe tener al menos 2 carácteres.')
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
        errors.append('El nombre sólo puede contener letras y espacios')

    if not last_name or len(last_name.strip()) < 2:
        errors.append('El apellido debe tener al menos 2 caracteres.')
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
        errors.append('El apellido solo puede contener letras y espacios.')

    if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
        errors.append('El email ingresado no es válido.')

    if membership_type not in ('silver', 'gold', 'platinum'):
        errors.append('El tipo de membresía no es válido.')

    return errors

def get_all_for_export():
    """Obtiene todos los afiliados activos para exportar a CSV"""
    with get_connection() as conn:
        return conn.execute(
            'SELECT afiliado_id, first_name, last_name, email, membership_type FROM afiliados WHERE estado = 1'
        ). fetchall()
