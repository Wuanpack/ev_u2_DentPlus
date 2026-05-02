"""Aplicación Principal"""
from flask import Flask, redirect, url_for
from models.afiliado import init_db
from controllers.afiliado_controller import afiliado_bp

# CREA LA APLICACIÓN Y USA APP.SECRET_KEY PARA QUE FLASK FUNCIONE CORRECTAMENTE CON FORMS
app = Flask(__name__)
app.secret_key = 'dentplus_secret_key'

# REGISTRA TODAS LAS RUTAS DEL CONTROLLER
app. register_blueprint(afiliado_bp)

# '/' REDIRIGE AUTOMÁTICAMENTE AL LISTADO DE AFILIADOS
@app.route('/')
def index():
    """Index"""
    return redirect(url_for('afiliados.index'))

# INIT_DB() CREA LA TABLA SI NO EXISTE Y DEBUG=TRUE REINICIA EL SERVIDOR CON CAMBIOS DE CÓDIGO
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
