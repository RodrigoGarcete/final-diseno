from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
from flask_session import Session
from conexion import conexion
import bcrypt
import os
from flask import jsonify
from functools import wraps
import json
from datetime import datetime

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
                if row['rol'] == 1:
                    return redirect(url_for('admin'))
                elif row['rol'] == 2:
                    return redirect(url_for('empleado'))
                elif row['rol'] == 3:
                    return redirect(url_for('cocinero'))


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

@app.route('/datos_menu', methods=['POST'])
@role_required(1)  # Requiere rol 1 (administrador)
def datos_menu():
    sql = "SELECT * FROM menu WHERE idmenu = %s"
    id = request.form.get('idmenu')
    with conexion.cursor() as cursor:
        cursor.execute(sql, (id,))
        menu = cursor.fetchone()
        
    print(id)
    datos = {
        'id': menu['idmenu'],
        'nombre': menu['nombre'],
        'descripcion': menu['descripcion'],
        'precio': menu['precio'],
        'idcategoria': menu['idcategoria'],
        'estado': menu['estado']
    }
    print(json.dumps(datos))
    return json.dumps(datos)
    
@app.route('/modificar_menu', methods=['POST'])
@role_required(1)  # Requiere rol 1 (administrador)
def modificar_menu():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')
    estado = request.form.get('estado')

    if 'imagen' in request.files:
        imagen = request.files['imagen']
        extension = imagen.filename.rsplit('.', 1)[1].lower()
        file = f"img-menu-{id}.{extension}"
        url_target = os.path.join(app.root_path, 'static/img/menus', file)
        imagen.save(url_target)
        sql2 = f"UPDATE menu SET nombre = '{nombre}', descripcion = '{descripcion}', precio = '{precio}', imagen = '{file}', idcategoria = '{categoria}', estado = '{estado}' WHERE idmenu = {id}"
    else:
        sql2 = f"UPDATE menu SET nombre = '{nombre}', descripcion = '{descripcion}', precio = '{precio}', idcategoria = '{categoria}', estado = '{estado}' WHERE idmenu = {id}"

    with conexion.cursor() as cursor:
        cursor.execute(sql2)
        conexion.commit()

    # Determine if the update was successful and create the response_data accordingly
    if cursor.rowcount > 0:
       return "1"
    else:
        return "ha habido un error"

@app.route('/guardarMenu', methods=['POST'])
@role_required(1)
def guardarMenu():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')
    estado = request.form.get('estado')

    if 'imagen' in request.files:
        sql = "SELECT MAX(idmenu) AS id FROM menu"
        with conexion.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            id = row['id'] + 1
        imagen = request.files['imagen']
        extension = imagen.filename.rsplit('.', 1)[1].lower()
        file = f"img-menu-{id}.{extension}"
        url_target = os.path.join(app.root_path, 'static/img/menus', file)
        imagen.save(url_target)
        fecha = datetime.now().strftime('%Y-%m-%d')
        sql2 = f"INSERT INTO menu (nombre, descripcion, precio, imagen, idcategoria, estado, fecha_creacion) VALUES ('{nombre}', '{descripcion}', '{precio}', '{file}', '{categoria}', '{estado}', '{fecha}')"
    else:
        sql2 = f"INSERT INTO menu (nombre, descripcion, precio, idcategoria, estado, fecha_creacion) VALUES ('{nombre}', '{descripcion}', '{precio}', '{categoria}', '{estado}', '{fecha}')"
    
    with conexion.cursor() as cursor:
        cursor.execute(sql2)
        conexion.commit()

    # Determine if the update was successful and create the response_data accordingly
    if cursor.rowcount > 0:
       return "1"
    else:
        return "ha habido un error"

@app.route('/ordenes', methods=['GET'])
@role_required(1)  # Requiere rol 1 (administrador)
def ordenes():
    sql = "SELECT * FROM categoria WHERE estado = 1 ORDER BY nombre ASC"
    with conexion.cursor() as cursor:
        cursor.execute(sql)
        categorias = cursor.fetchall()

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    sql_facturacion = "SELECT * FROM facturacion WHERE fecha = %s ORDER BY hora DESC"
    with conexion.cursor() as cursor:
        cursor.execute(sql_facturacion, (fecha_actual,))
        factura_data = cursor.fetchall()

    return render_template('admin/ordenes.html', categorias=categorias, factura_data=factura_data)

@app.route('/usuarios', methods=['GET'])
@role_required(1)  # Requiere rol 1 (administrador)
def usuarios():
    with conexion.cursor() as cursor:
        query = "SELECT * FROM usuario"
        cursor.execute(query)
        usuarios = cursor.fetchall()

    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/menu')
@role_required(1)  # Requiere rol 1 (administrador)
def menu_admin():
    sql = "SELECT * FROM categoria"
    with conexion.cursor() as cursor:
        cursor.execute(sql)
        categorias = cursor.fetchall()
    
    sql_menus = "SELECT menu.*, categoria.nombre AS categoria_nombre FROM menu INNER JOIN categoria ON menu.idcategoria = categoria.idcategoria"
    with conexion.cursor() as cursor:
        cursor.execute(sql_menus)
        menus = cursor.fetchall()
    return render_template('admin/menu.html', categorias=categorias, menu_rows=menus)

@app.route('/empleado')
def empleado():
    return "Página de empleado"

@app.route('/cocinero')
def cocinero():
    return "Página de cocinero"

@app.route('/datos_usuario', methods=['POST'])
def datos_usuario():
    idusuario = request.form.get('idusuario')
    
    # Realiza la consulta a la base de datos para obtener los datos del usuario
    sql = f"SELECT * FROM usuario WHERE idusuario = {idusuario}"
    with conexion.cursor() as cursor:
        cursor.execute(sql)
        usuario = cursor.fetchone()
    
    if usuario:
        # Formatea los datos del usuario en un diccionario
        datos_usuario = {
            'idusu': usuario['idusuario'],
            'nombre': usuario['nombre'],
            'apellido': usuario['apellido'],
            'usuario': usuario['usuario'],
            'rol': usuario['rol'],
            'estado': usuario['estado']
        }
        return json.dumps(datos_usuario), 200
    else:
        return json.dumps({'error': 'Usuario no encontrado'}), 404

@app.route('/modificar_usuario', methods=['POST'])
def modificar_usuario():
    idusuario = request.form.get('id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    usuario = request.form.get('usuario')
    rol = request.form.get('rol')
    estado = request.form.get('estado')
    
    password = request.form.get('pass')
    if password:
        # Generar un hash seguro de la contraseña
        password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        consulta = "UPDATE usuario SET nombre = %s, apellido = %s, usuario = %s, rol = %s, estado = %s, pass = %s WHERE idusuario = %s"
        parametros = (nombre, apellido, usuario, rol, estado, password_hashed, idusuario)
    else:
        consulta = "UPDATE usuario SET nombre = %s, apellido = %s, usuario = %s, rol = %s, estado = %s WHERE idusuario = %s"
        parametros = (nombre, apellido, usuario, rol, estado, idusuario)
        
    with conexion.cursor() as cursor:
        cursor.execute(consulta, parametros)
        conexion.commit()
    
    if cursor.rowcount > 0:
        return "1"
    else:
        return "0"







@app.route('/cerrar_session', methods=['POST'])
def cerrar_session():
    # Destruir la sesión
    session.clear()
    return jsonify(1)

if __name__ == '__main__':
    app.run(debug=True)
