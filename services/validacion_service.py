"""Servicio de validaciones"""
import re
from models.afiliado import get_by_email

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

def validar_email_unico(email, afiliado_id=None):
    """Valida que un email sea único, comparandolo con la BBDD"""
    afiliado_existente = get_by_email(email)
    if not afiliado_existente:
        return None

    if afiliado_id and afiliado_existente['afiliado_id'] == afiliado_id:
        return None

    return 'El email ingresado ya está registrado'
