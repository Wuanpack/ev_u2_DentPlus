"""Cálculos de la app"""

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
