"""Módulo Controller para lógica de rutas y coordinación HTTP"""
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
import models.afiliado as afiliado_model

afiliado_bp = Blueprint('afiliados', __name__)

@afiliado_bp.route('/afiliados')
def index():
    """Obtiene todos los afiliados con la función get_all de models/afiliado.py"""
    afiliados = afiliado_model.get_all()
    return render_template('afiliados/index.html', afiliados=afiliados)

@afiliado_bp.route('/afiliados/nuevo', methods=['GET', 'POST'])
def crear():
    """Crea un afiliado con la función create de models/afiliado.py"""
    error = None
    if request.method == 'POST':
        try:
            afiliado_model.create(
                request.form['first_name'],
                request.form['last_name'],
                request.form['email'],
                request.form['membership_type']
            )
            return redirect(url_for('afiliados.index'))
        except sqlite3.IntegrityError as e:
            print(f"Error al crear afiliado: {e}")
            error = 'El email ingresado ya está registrado.'
    return render_template('afiliados/formulario.html', afiliado=None, error=error)

@afiliado_bp.route('/afiliados/<int:afiliado_id>')
def detalle(afiliado_id):
    """Muestra el detalle de un afiliado en específico usando la función get_by_id(id)"""
    afiliado = afiliado_model.get_by_id(afiliado_id)
    descuento = None
    total = None

    if request.args.get('monto'):
        monto = float(request.args.get('monto'))
        descuento, total = afiliado_model.calcular_descuento(afiliado['membership_type'], monto)

    return render_template('afiliados/detalle.html', afiliado=afiliado, descuento=descuento, total=total)

@afiliado_bp.route('/afiliados/<int:afiliado_id>/editar', methods=['GET', 'POST'])
def editar(afiliado_id):
    """Edita un usuario usando get_by_id"""
    afiliado = afiliado_model.get_by_id(afiliado_id)
    if request.method == 'POST':
        afiliado_model.update(
            afiliado_id,
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form['membership_type']
        )
        return redirect(url_for('afiliados.detalle', afiliado_id=afiliado_id))
    return render_template('afiliados/formulario.html', afiliado=afiliado)

@afiliado_bp.route('/afiliados/<int:afiliado_id>/desactivar', methods=['POST'])
def desactivar(afiliado_id):
    """Desactiva un usuario por medio de su id"""
    afiliado_model.deactivate(afiliado_id)
    return redirect(url_for('afiliados.index'))

@afiliado_bp.route('/afiliados/inactivos')
def inactivos():
    """Obtiene todos los usuarios inactivos"""
    afiliados = afiliado_model.get_all_inactive()
    return render_template('afiliados/inactivos.html', afiliados=afiliados)

@afiliado_bp.route('/afiliados/<int:afiliado_id>/activar', methods=['POST'])
def activar(afiliado_id):
    """Reactiva un afiliado por medio de su afiliado_id"""
    afiliado_model.activate(afiliado_id)
    return redirect(url_for('afiliados.inactivos'))
