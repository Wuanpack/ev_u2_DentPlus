import sqlite3

DB_PATH = 'dentplus.db'

# INICIA LA CONEXIÓN CON LA BASE DE DATOS
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS afiliados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                membershipType TEXT NOT NULL CHECK(membershipType IN ('silver', 'gold', 'platinum')),
                estado INTEGER NOT NULL DEFAULT 1
                )
        ''')

# OBTENER TODOS LOS AFILIADOS ACTIVOS
def get_all():
    with get_connection() as conn:
        return conn.execute('SELECT * FROM afiliados WHERE estado = 1').fetchall()

# OBTENER TODOS LOS AFILIADOS INACTIVOS
def get_all_inactive():
    with get_connection() as conn:
        return conn.execute('SELECT * FROM afiliados WHERE estado = 0').fetchall()

# OBTENER AFILIADOS POR ID
def get_by_id(id):
    with get_connection() as conn:
        return conn.execute('SELECT * FROM afiliados WHERE id = ?', (id,)).fetchone()

# CREAR AFILIADOS
def create(firstName, lastName, email, membershipType):
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO afiliados (firstName, lastName, email, membershipType) VALUES (?,?,?,?)',
            (firstName, lastName, email, membershipType)
        )

# MODIFICAR UN AFILIADO SEGÚN ID
def update(id, firstName, lastName, email, membershipType):
    with get_connection() as conn:
        conn.execute(
            'UPDATE afiliados SET firstName=?, lastName=?, email=?, membershipType=? WHERE id=?',
            (firstName, lastName, email, membershipType, id)
        )

# DESACTIVAR UN AFILIADO POR ID
def deactivate(id):
    with get_connection() as conn:
        conn.execute('UPDATE afiliados SET estado = 0 WHERE id=?', (id,))

# CALCULAR EL DESCUENTO SEGÚN EL TIPO DE MEMBRESÍA Y EL MONTO
def calcular_descuento(membershipType, monto):
    descuentos = {
        'silver': 0.05,
        'gold': 0.10,
        'platinum': 0.20
    }
    porcentaje = descuentos.get(membershipType, 0)
    descuento = monto * porcentaje
    total = monto - descuento
    return round(descuento, 2), round(total, 2)