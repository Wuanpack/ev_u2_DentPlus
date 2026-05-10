"""Módulo Controller para lógica de rutas y coordinación HTTP"""
import sqlite3
import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import models.afiliado as afiliado_model
from services.validacion_service import validar_afiliado, validar_email_unico
from services.descuento_service import calcular_descuento

afiliado_bp = Blueprint('afiliados', __name__)

@afiliado_bp.route('/afiliados')
def index():
    """Obtiene todos los afiliados con la función get_all de models/afiliado.py"""
    search = request.args.get('search', '')
    membership_type = request.args.get('membership_type', '')
    afiliados = afiliado_model.get_all(
        search=search or None,
        membership_type=membership_type or None
    )
    return render_template('afiliados/index.html',
        afiliados=afiliados,
        search=search,
        membership_type=membership_type or None
    )

@afiliado_bp.route('/afiliados/nuevo', methods=['GET', 'POST'])
def crear():
    """Crea un usuario usando la función create de models/afiliado.py"""
    errors = []
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        membership_type = request.form['membership_type']

        errors = validar_afiliado(first_name, last_name, email, membership_type)
        error_email = validar_email_unico(email)
        if error_email:
            errors.append(error_email)

        if not errors:
            try:
                afiliado_model.create(first_name, last_name, email, membership_type)
                flash('Afiliado creado correctamente.', 'success')
                return redirect(url_for('afiliados.index'))
            except sqlite3.IntegrityError as e:
                errors.append('El email ingresado ya está registrado.')

    return render_template('afiliados/formulario.html', afiliado=None, errors=errors)


@afiliado_bp.route('/afiliados/<int:afiliado_id>')
def detalle(afiliado_id):
    """Muestra el detalle de un afiliado en específico usando la función get_by_id(id)"""
    afiliado = afiliado_model.get_by_id(afiliado_id)
    descuento = None
    total = None

    if request.args.get('monto'):
        monto = float(request.args.get('monto'))
        descuento, total = calcular_descuento(afiliado['membership_type'], monto)

    return render_template('afiliados/detalle.html', afiliado=afiliado, descuento=descuento, total=total)

@afiliado_bp.route('/afiliados/<int:afiliado_id>/editar', methods=['GET', 'POST'])
def editar(afiliado_id):
    """Modifica los datos de un afiliado dependiendo de su afiliado_id"""
    afiliado = afiliado_model.get_by_id(afiliado_id)
    errors = []
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        membership_type = request.form['membership_type']

        errors = validar_afiliado(first_name, last_name, email, membership_type)
        error_email = validar_email_unico(email, afiliado_id)
        if error_email:
            errors.append(error_email)

        if not errors:
            afiliado_model.update(afiliado_id, first_name, last_name, email, membership_type)
            flash('Afiliado actualizado correctamente.', 'success')
            return redirect(url_for('afiliados.detalle', afiliado_id=afiliado_id))

    return render_template('afiliados/formulario.html', afiliado=afiliado, errors=errors)

@afiliado_bp.route('/afiliados/<int:afiliado_id>/desactivar', methods=['POST'])
def desactivar(afiliado_id):
    """Desactiva un usuario por medio de su id"""
    afiliado_model.deactivate(afiliado_id)
    flash('Afiliado desactivado', 'warning')
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
    flash('Afiliado reactivado correctamente', 'success')
    return redirect(url_for('afiliados.inactivos'))

@afiliado_bp.route('/afiliados/exportar')
def exportar_csv():
    """Exporta el listado de afiliados activos a CSV"""
    afiliados = afiliado_model.get_all_for_export()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['ID', 'Nombre', 'Apellido', 'Email', 'Membresía'])
    for afiliado in afiliados:
        writer.writerow([
            afiliado['afiliado_id'],
            afiliado['first_name'],
            afiliado['last_name'],
            afiliado['email'],
            afiliado['membership_type']
        ])

    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=afiliados_dentplus.csv'}
    )
