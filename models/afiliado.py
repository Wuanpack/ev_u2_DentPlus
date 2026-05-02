import sqlite3

DB_PATH = 'dentplus.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
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
    conn.commit()
    conn.close()

def get_all():
    conn = get_connection()
    afiliados = conn.execute('SELECT * FROM afiliados WHERE estado = 1').fetchall()
    conn.close()
    return afiliados

def get_all_inactive():
    conn = get_connection()
    afiliados = conn.execute('SELECT * FROM afiliados WHERE estado = 0').fetchall()
    conn.close()
    return afiliados

def get_by_id(id):
    conn = get_connection()
    afiliado = conn.execute('SELECT * FROM afiliados WHERE id = ?', (id,)).fetchone()
    conn.close()
    return afiliado

def create(firstName, lastName, email, membershipType):
    conn = get_connection()
    conn.execute(
        'INSERT INTO afiliados (firstName, lastName, email, membershipType) VALUES (?,?,?,?)',
        (firstName, lastName, email, membershipType)
    )
    conn.commit()
    conn.close()

def update(id, firstName, lastName, email, membershipType):
    conn = get_connection()
    conn.execute(
        'UPDATE afiliados SET firstName=?, lastName=?, email=?, membershipType=? WHERE id=?',
        (firstName, lastName, email, membershipType, id)
    )
    conn.commit()
    conn.close()

def deactivate(id):
    conn = get_connection()
    conn.execute('UPDATE afiliados SET estado = 0 WHERE id=?', (id,))
    conn.commit()
    conn.close()

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