from flask import Blueprint, render_template, request, redirect, url_for
import models.afiliado as afiliado_model

afiliado_bp = Blueprint('afiliados', __name__)

@afiliado_bp.route('/afiliados')
def index():
    afiliado = afiliado_model.get_by_id(id)
    descuento = None
    total = None

    if request.args.get('monto'):
        monto = float(request.args.get('monto'))
        descuento, total = afiliado_model.calcular_descuento(afiliado ['membershipType'], monto)

        return render_template('afiliados/detalle.html', afiliado=afiliado, descuento=descuento, total=total)

@afiliado_bp.route('/afiliados/nuevo', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        afiliado_model.create(
            request.form['firstName'],
            request.form['lastName'],
            request.form['email'],
            request.form['membershipType']
        )
        return redirect(url_for(afiliados.index))
    return render_template('afiliados/formulario.html', afiliado=None)

@afiliado_bp.route('/afiliados/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    afiliado = afiliado_model.get_by_id(id)
    if request.method == 'POST':
        afiliado_model.update(
            id,
            request.form['firstName'],
            request.form['lastName'],
            request.form['email'],
            request.form['membershipType']
        )
        return redirect(url_for('afiliados.detalle', id=id))
    return render_template('afiliados/formulario.html', afiliado=afiliado)

@afiliado_bp.route('/afiliados/<int:id>/desactivar', methods=['POST'])
def desactivar(id):
    afiliado_model.deactivate(id)
    return redirect(url_for('afiliados.index'))

