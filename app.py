from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
from flask_session import Session
from conexion import conexion
import bcrypt
import os
from flask import jsonify
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configuración de la sesión
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Decorador para verificar el rol del usuario
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if 'usuario' in session and 'rol' in session and session['rol'] == role:
                return view_func(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        return wrapped_view
    return decorator

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        # Si ya hay una sesión de usuario, redirigir según el rol
        rol = session['rol']
        if rol == 1:
            return redirect(url_for('admin'))
        elif rol == 2:
            return redirect(url_for('empleado'))
        elif rol == 3:
            return redirect(url_for('cocinero'))

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['pass']

        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuario WHERE usuario = %s"
            cursor.execute(sql, (usuario,))
            row = cursor.fetchone()

            if row and row['estado'] == 1 and bcrypt.checkpw(password.encode('utf-8'), row['pass'].encode('utf-8')):
                session['idusuario'] = row['idusuario']
                session['usuario'] = row['usuario']
                session['rol'] = row['rol']
                session['estado'] = row['estado']
                session['nombre'] = row['nombre']
                session['apellido'] = row['apellido']
                return redirect(url_for('admin'))

    return render_template('login.html', alerta="Usuario o contraseña incorrectos.")

@app.route('/categoriasadmin', methods=['GET', 'POST'])
@role_required(1)  # Requiere rol 1 (administrador)
def categoriasadmin():
    if 'usuario' in session and 'rol' in session:
        if session['rol'] == 1:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM categoria"
                cursor.execute(sql)
                categorias = cursor.fetchall()
            return render_template('admin/categorias.html', categorias=categorias)
    return "Acceso no autorizado"

@app.route('/datoscategoria', methods=['GET','POST'])
@role_required(1)  # Requiere rol 1 (administrador)
def datoscategoria():
    
    id = request.form.get('id')
    sql = "SELECT * FROM categoria WHERE idcategoria = %s"
    #print("Consulta SQL:", sql % id)
    with conexion.cursor() as cursor:
        cursor.execute(sql, (id,))
        categoria = cursor.fetchone()
    
    categoria_dict = {
        'idcategoria': categoria['idcategoria'],
        'nombre': categoria['nombre'],
        'descripcion': categoria['descripcion'],
        'fecha_creacion': categoria['fecha_creacion'].strftime('%d/%m/%Y'),
        'estado': categoria['estado']
    }
    print(json.dumps(categoria_dict))
    return json.dumps(categoria_dict)

@app.route('/modificarCategoria', methods=['POST'])  # Definimos la ruta y los métodos permitidos
def modificar_categoria():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    estado = request.form.get('estado')
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE categoria SET nombre = %s, descripcion = %s, estado = %s WHERE idcategoria = %s"
            cursor.execute(sql, (nombre, descripcion, estado, id))
            conexion.commit()
        respuesta = 1
    except:
        respuesta = 0

    return str(respuesta)

@app.route('/guardarCategoria', methods=['POST'])  # Definimos la ruta y los métodos permitidos
def guardar_categoria():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    estado = request.form.get('estado')

    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO categoria (nombre, descripcion, estado, fecha_creacion) VALUES (%s, %s, %s, CURDATE())"
            cursor.execute(sql, (nombre, descripcion, estado))
            conexion.commit()
       
        guardado_exitoso = 1

        return str(guardado_exitoso)

    except Exception as e:
        return '0'




@app.route('/admin', methods=['GET'])
@role_required(1)  # Requiere rol 1 (administrador)
def admin():
    if 'usuario' in session and 'rol' in session:
        if session['rol'] == 1:
            with conexion.cursor() as cursor:
                # Consulta total ventas de hoy horario paraguay
                sql_total_ventas = "SELECT SUM(total) AS total FROM facturacion WHERE fecha = CURDATE()"
                cursor.execute(sql_total_ventas)
                row_total_ventas = cursor.fetchone()
                if row_total_ventas and row_total_ventas['total'] is not None:
                    total_ventas = '{:,.0f}'.format(row_total_ventas['total'])
                else:
                    total_ventas = '0'


                # Consulta total categorias
                sql_total_categorias = "SELECT COUNT(*) AS total FROM categoria"
                cursor.execute(sql_total_categorias)
                row_total_categorias = cursor.fetchone()

                # Consulta total menús
                sql_total_menus = "SELECT COUNT(*) AS total FROM menu"
                cursor.execute(sql_total_menus)
                row_total_menus = cursor.fetchone()

                # Consulta total órdenes en cola
                sql_total_ordenes = "SELECT COUNT(*) AS total FROM facturacion WHERE estado = '0'"
                cursor.execute(sql_total_ordenes)
                row_total_ordenes = cursor.fetchone()

                # Consulta menús más vendidos hoy
                sql_top_menus = """
                    SELECT m.nombre, SUM(df.cantidad) AS total_vendidas
                    FROM facturacion f
                    INNER JOIN detalle_facturacion df ON df.idfacturacion = f.idfacturacion
                    INNER JOIN menu m ON m.idmenu = df.idmenu
                    WHERE f.fecha = CURDATE()
                    GROUP BY df.idmenu, f.fecha
                    ORDER BY total_vendidas DESC
                    LIMIT 4;
                """
                cursor.execute(sql_top_menus)
                top_menus = cursor.fetchall()

                # Consulta ventas por meses
                sql_ventas_meses = """
                    SELECT MONTH(fecha) AS mes, SUM(total) AS total
                    FROM facturacion
                    GROUP BY MONTH(fecha)
                    ORDER BY MONTH(fecha) DESC
                    LIMIT 5;
                """
                cursor.execute(sql_ventas_meses)
                ventas_meses = cursor.fetchall()

            return render_template(
                'admin/admin.html',
                total_ventas=total_ventas,
                total_categorias=row_total_categorias['total'],
                total_menus=row_total_menus['total'],
                total_ordenes=row_total_ordenes['total'],
                top_menus=top_menus,
                ventas_meses=ventas_meses
            )

    return "Acceso no autorizado"

@app.route('/empleado')
def empleado():
    return "Página de empleado"

@app.route('/cocinero')
def cocinero():
    return "Página de cocinero"

@app.route('/cerrar_session', methods=['POST'])
def cerrar_session():
    # Destruir la sesión
    session.clear()
    return jsonify(1)

if __name__ == '__main__':
    app.run(debug=True)
