from flask import Flask, render_template, request, redirect, url_for, session, Response,send_file
import pymysql.cursors
from flask_session import Session
from conexion import conexion
import bcrypt
import os
from flask import jsonify
from functools import wraps
import json
from datetime import datetime
import pytz
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
import io
#import httresponse


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
@role_required(2)  # Requiere rol 2 (empleado)
def empleado():
    if 'usuario' in session and 'rol' in session:
        if session['rol'] == 2:  
            with conexion.cursor() as cursor:
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

            return render_template(
                'empleado/empleado.html',
                total_categorias=row_total_categorias['total'],
                total_menus=row_total_menus['total'],
                total_ordenes=row_total_ordenes['total']
            )

    return "Acceso no autorizado"

@app.route('/filtrar_menus', methods=['POST'])
@role_required(2)  # Requiere rol 2 (empleado)
def filtrar_menus():
    categoria = request.form.get('categoria')
    buscar = request.form.get('buscar')
    #si categoria es distinto a 0
    if categoria != '0':
        sql = """SELECT menu.idmenu,menu.descripcion,menu.imagen,menu.nombre as menu,menu.precio,categoria.nombre as categoria, menu.estado as estado_menu, categoria.estado as estado_categoria
        FROM menu inner join categoria on menu.idcategoria = categoria.idcategoria WHERE menu.nombre LIKE '%{buscar}%' AND menu.estado = 1 AND categoria.estado = 1 and menu.idcategoria = {categoria}"""
    else:
        sql = """SELECT menu.idmenu,menu.descripcion,menu.imagen,menu.nombre as menu,menu.precio,categoria.nombre as categoria, menu.estado as estado_menu, categoria.estado as estado_categoria
        FROM menu inner join categoria on menu.idcategoria = categoria.idcategoria WHERE menu.nombre LIKE '%{buscar}%' AND menu.estado = 1 
        AND categoria.estado = 1"""
    with conexion.cursor() as cursor:
        cursor.execute(sql.format(buscar=buscar, categoria=categoria))
        menus = cursor.fetchall()
    
    if menus:
        html_result = ""
        for row in menus:
            imagen = row['imagen']
            idmenu = row['idmenu']
            nombre = row['menu']
            descripcion = row['descripcion']
            #precio con numberformat python
            precio = row['precio']
            html_result += f"""<div class="col my-2">
                        <div class="card shadow p-1 bg-body rounded">
                        <img src="static/img/menus/{imagen}" alt="imagen" width="100%" height="150">
                        <div class="card-body p-2">
                        <p class="card-title my-1" id="nombre-menu-{idmenu}">{nombre}</p>
                        <p class="card-text"><b>Precio: </b><span id="precio-menu-{idmenu}">{precio}</span> Gs</p>
                        <p class="card-text lh-sm text-truncate">'{descripcion}"{descripcion}</p>
                        <a data-bs-toggle="tooltip" data-bs-title="{descripcion}"><i class="bi bi-info-circle"></i></a>
                        <div class="d-flex justify-content-between align-items-center">
                        <div class="btn-group mx-auto">
                        <button type="button" class="boton-pedido" onclick="agregarProducto({idmenu})">Agregar</button>
                        </div></div></div></div></div>
                    """
    else:
        html_result = """<div class="col my-2">
                        <div class="card shadow p-1 bg-body rounded">
                            <div class="card-body p-2">
                                <p class="card-title my-1">No se encontraron resultados</p>
                            </div>
                        </div>
                    </div>"""
    return html_result

@app.route('/buscar_cliente', methods=['POST'])
@role_required(2)  # Requiere rol 2 (empleado)
def buscar_cliente():
    ruc = request.form.get('ruc')
    sql = "SELECT * FROM cliente WHERE ruc = %s"
    with conexion.cursor() as cursor:
        cursor.execute(sql, (ruc,))
        cliente = cursor.fetchone()
    
    if cliente:
        datos_cliente = {
            'id': cliente['idcliente'],
            'nombre': cliente['nombre'],
            'apellido': cliente['apellido']
        }
    else:
        datos_cliente = {
            'id': 0,
            'nombre': 'No existe',
            'apellido': ' '
        }
    return json.dumps(datos_cliente), 200

@app.route('/facturar', methods=['POST'])
@role_required(2)  # Requiere rol 2 (empleado)
def facturar():
    
    data = request.json
    idcliente = data.get("idcliente")
    total = data.get("total")
    efectivo = data.get("efectivo")
    vuelto = data.get("vuelto")
    idusuario = data.get("idusuario")
    idmenuArray = data.get("idmenu")
    cantidadArray = data.get("cantidad")
    precioArray = data.get("precio")

    tz = pytz.timezone('America/Asuncion')
    fecha_actual = datetime.now(tz).strftime('%Y-%m-%d')
    hora_actual = datetime.now(tz).strftime('%H:%M:%S')

    error = 0

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM facturacion WHERE fecha = %s ORDER BY idfacturacion DESC LIMIT 1", (fecha_actual,))
        row = cursor.fetchone()
        
        if row:
            nro_orden = row['orden'] + 1
        else:
            nro_orden = 1

        conexion.begin()

        cursor.execute("INSERT INTO facturacion (idcliente, total, fecha, hora, idusuario, estado, orden) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (idcliente, total, fecha_actual, hora_actual, idusuario, '0', nro_orden))
        idfactura = cursor.lastrowid

        for i in range(len(idmenuArray)):
            precio = precioArray[i].replace(".", "")
            cursor.execute("INSERT INTO detalle_facturacion (idfacturacion, idmenu, cantidad, precio) VALUES (%s, %s, %s, %s)",
                           (idfactura, idmenuArray[i], cantidadArray[i], precio))

        conexion.commit()

        if cursor.rowcount > 0:
            response_data = {
                'idfactura': idfactura,
                'nro_orden': nro_orden,
                'efectivo': efectivo,
                'vuelto': vuelto,
                'error': error,
                'fecha': fecha_actual,
                'hora': hora_actual
            }
        else:
            conexion.rollback()
            error = 1
            response_data = {'error': error}

    return json.dumps(response_data), 200

    

@app.route('/pedido', methods=['GET'])
@role_required(2)  # Requiere rol 2 (empleado)
def pedido():
    sql = "SELECT * FROM categoria WHERE estado = 1"
    with conexion.cursor() as cursor:
        cursor.execute(sql)
        categorias = cursor.fetchall()
    
    with conexion.cursor() as cursor:
        sql = "SELECT *,menu.descripcion as menu_descripcion,menu.nombre as menu_nombre FROM menu inner join categoria on menu.idcategoria = categoria.idcategoria WHERE menu.estado = 1 and categoria.estado = 1"
        cursor.execute(sql)
        menus = cursor.fetchall()

    idusuario = session.get('idusuario')
    nombre = session.get('nombre')
    apellido = session.get('apellido')
    return render_template('empleado/pedido.html', categorias=categorias, menus=menus, idusuario=idusuario, nombre=nombre, apellido=apellido)

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

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    usuario = request.form.get('usuario')
    rol = request.form.get('rol')
    estado = request.form.get('estado')
    password = request.form.get('password')
    fecha = datetime.now().strftime('%Y-%m-%d')
    print(password)

    # Generar un hash seguro de la contraseña
    password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    consulta = "INSERT INTO usuario (nombre, apellido, usuario, rol, estado, pass, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())"
    parametros = (nombre, apellido, usuario, rol, estado, password_hashed)
        
    with conexion.cursor() as cursor:
        cursor.execute(consulta, parametros)
        conexion.commit()
    
    if cursor.rowcount > 0:
        return "1"
    else:
        return "0"

@app.route('/ticket', methods=['POST'])
def generate_pdf():
    # Crear el objeto PDF
    response = Response(content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    #imprimir request
    print(request.get_json())
    
    data = request.get_json()

    idcliente = data['idcliente']
    total = data['total']
    efectivo = data['efectivo']
    vuelto = data['vuelto']
    idfactura = data['idfactura']
    nombre_empleado = data['nombre_empleado']
    cantidad = data['cantidad']
    precios = data['precio']
    menu = data['menu']
    fecha_actual = data['fecha_actual']
    hora_actual = data['hora_actual']
    nro_orden = data['nro_orden']

    sql = "SELECT * FROM cliente WHERE idcliente = %s"
    with conexion.cursor() as cursor:
        cursor.execute(sql, (idcliente,))
        cliente = cursor.fetchone()
    #si apellido es none
    if cliente['apellido'] is None:
        nombre_apellido = cliente['nombre']
        ruc = cliente['ruc']
    else:
        nombre_apellido = cliente['nombre'] + ' ' + cliente['apellido']
        ruc = cliente['ruc']

    pdf_output = io.BytesIO()

    c = canvas.Canvas(pdf_output)
    #tamano ajustado al texto
    c.setPageSize((300, 800))

    # CABECERA
    
    c.setFont('Helvetica', 12)
    c.drawString(60, 700, 'Comidas RyN')
    c.setFont('Helvetica', 8)
    c.drawString(60, 690, 'COMIDAS RAPIDAS RyN')
    c.setFont('Helvetica', 7)
    c.drawString(60, 680, 'de Rodrigo y Nathalia')
    c.setFont('Helvetica', 5)
    c.drawString(60, 670, 'Calle Mcal Lopez c/ Mauricio Jose Troche')
    c.drawString(60, 660, 'Cel: 0976-415982')
    
    c.setFont('Helvetica', 7)
    idfactura = str(idfactura).zfill(7)
    fecha_estil = fecha_actual.replace("-", "")
    num = fecha_estil + idfactura
    c.drawString(60, 640, 'Nro Factura: ' + num)
    c.drawString(60, 630, 'Fecha: ' + fecha_actual)
    c.drawString(60, 620, 'Hora: ' + hora_actual)
    c.drawString(60, 610, 'Cod.Cliente: ' + idcliente)
    c.drawString(60, 600, 'Cliente: ' + nombre_apellido)
    c.drawString(60, 590, 'Ruc/Ci: ' + str(ruc))
    c.drawString(60, 580, 'Empleado: ' + nombre_empleado)

    c.drawString(60, 560, '-------------------------------------------------------------------------------')

    # Cabecera tabla
    c.setFont('Helvetica', 6)
    c.drawString(60, 540, 'Cant.')
    c.drawString(80, 540, 'Descripcion')
    c.drawString(160, 540, 'Precio')
    c.drawString(220, 540, 'Importe')
    c.setFont('Helvetica', 7)
    c.drawString(60, 530, '-------------------------------------------------------------------------------')
    c.setFont('Helvetica', 6)
    
    # Recorrer arrays
    y_position = 510
    for i in range(len(cantidad)):
        c.drawString(60, y_position, cantidad[i])
        c.drawString(80, y_position, menu[i])
        c.drawString(160, y_position, precios[i])
        importe = str(float(precios[i].replace('.', '')) * int(cantidad[i]))
        c.drawString(220, y_position, importe)
        y_position -= 10

    c.setFont('Helvetica', 7)
    c.drawString(60, y_position - 10, '-------------------------------------------------------------------------------')

    # Totales
    c.setFont('Helvetica', 7)
    c.drawString(190, y_position - 30, 'Total: ' + total)
    c.drawString(190, y_position - 40, 'Efectivo: ' + efectivo)
    c.drawString(190, y_position - 50, 'Vuelto: ' + vuelto)
    c.drawString(100, y_position - 70, 'Nro Orden: #' + str(nro_orden))
    
    c.setFont('Helvetica', 6)
    c.drawString(100, y_position - 80, 'Iva incluido')
    c.drawString(100, y_position - 90, 'Gracias por su compra')

    c.showPage()
    c.save()
    pdf_output.seek(0)
    
    # Devolver la respuesta al cliente
    return Response(pdf_output, content_type='application/pdf',
                        headers={'Content-Disposition': 'inline; filename=factura.pdf'})


@app.route('/cerrar_session', methods=['POST'])
def cerrar_session():
    # Destruir la sesión
    session.clear()
    return jsonify(1)

if __name__ == '__main__':
    app.run(debug=True)
