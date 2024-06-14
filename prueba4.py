import tkinter as tk
from tkinter import messagebox
import json
import os

# Archivos JSON
ARCHIVO_PRODUCTOS = 'productos.json'
ARCHIVO_USUARIOS = 'usuarios.json'
ARCHIVO_COMPRAS = 'compras.json'
ARCHIVO_REPOSICIONES = 'reposiciones.json'
ARCHIVO_PROVEEDORES = 'proveedores.json'

# Datos globales
productos = []
usuarios = {}
compras = {}
carrito = []
reposiciones = []
proveedores = []

# Credenciales del gerente por defecto
NOMBRE_GERENTE = "gerente"
CONTRASENA_GERENTE = "gerente123"

def cargar_datos():
    """Carga los datos de productos, usuarios, compras, reposiciones y proveedores desde los archivos JSON, si existen."""
    global productos, usuarios, compras, reposiciones, proveedores
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, 'r') as archivo:
            productos = json.load(archivo)
    else:
        productos = []

    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, 'r') as archivo:
            usuarios = json.load(archivo)
    else:
        usuarios = {
            NOMBRE_GERENTE: {
                'contrasena': CONTRASENA_GERENTE,
                'rol': 'gerente'
            }
        }
        guardar_usuarios()

    if os.path.exists(ARCHIVO_COMPRAS):
        with open(ARCHIVO_COMPRAS, 'r') as archivo:
            compras = json.load(archivo)
    else:
        compras = {}
        
    if os.path.exists(ARCHIVO_REPOSICIONES):
        with open(ARCHIVO_REPOSICIONES, 'r') as archivo:
            reposiciones = json.load(archivo)
    else:
        reposiciones = []

    if os.path.exists(ARCHIVO_PROVEEDORES):
        with open(ARCHIVO_PROVEEDORES, 'r') as archivo:
            proveedores = json.load(archivo)
    else:
        proveedores = []

def guardar_productos():
    """Guarda los datos de productos en el archivo JSON."""
    with open(ARCHIVO_PRODUCTOS, 'w') as archivo:
        json.dump(productos, archivo, indent=4)

def guardar_usuarios():
    """Guarda los usuarios en el archivo JSON."""
    with open(ARCHIVO_USUARIOS, 'w') as archivo:
        json.dump(usuarios, archivo, indent=4)

def guardar_compras():
    """Guarda las compras en el archivo JSON."""
    with open(ARCHIVO_COMPRAS, 'w') as archivo:
        json.dump(compras, archivo, indent=4)

def guardar_reposiciones():
    """Guarda los reportes de reposición en el archivo JSON."""
    with open(ARCHIVO_REPOSICIONES, 'w') as archivo:
        json.dump(reposiciones, archivo, indent=4)

def guardar_proveedores():
    """Guarda los proveedores en el archivo JSON."""
    with open(ARCHIVO_PROVEEDORES, 'w') as archivo:
        json.dump(proveedores, archivo, indent=4)

def agregar_producto(nombre, precio, cantidad):
    """Agrega un nuevo producto al archivo JSON."""
    global productos
    if not nombre or not precio or not cantidad:
        raise ValueError("Todos los campos son obligatorios.")
    
    try:
        precio = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        raise ValueError("El precio debe ser un número y la cantidad un entero.")

    for producto in productos:
        if producto['nombre'] == nombre:
            raise ValueError("El producto ya existe.")

    productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
    guardar_productos()

def modificar_producto(nombre, precio, cantidad):
    """Modifica un producto existente en el archivo JSON."""
    global productos
    if not nombre:
        raise ValueError("El nombre del producto es obligatorio.")
    
    try:
        precio = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        raise ValueError("El precio debe ser un número y la cantidad un entero.")

    for producto in productos:
        if producto["nombre"] == nombre:
            producto["precio"] = precio
            producto["cantidad"] = cantidad
            guardar_productos()
            return
    raise ValueError("Producto no encontrado.")

def eliminar_producto(nombre):
    """Elimina un producto del archivo JSON."""
    global productos
    if not nombre:
        raise ValueError("El nombre del producto es obligatorio.")

    for producto in productos:
        if producto["nombre"] == nombre:
            productos.remove(producto)
            guardar_productos()
            return
    raise ValueError("Producto no encontrado.")

def listar_productos():
    """Devuelve una lista de todos los productos."""
    global productos
    return productos

def agregar_usuario(nombre_usuario, contrasena, rol='cliente'):
    """Agrega un nuevo usuario al archivo JSON."""
    global usuarios
    if not nombre_usuario or not contrasena:
        raise ValueError("Todos los campos son obligatorios.")

    if nombre_usuario in usuarios:
        raise ValueError("El nombre de usuario ya existe.")

    usuarios[nombre_usuario] = {
        'contrasena': contrasena,
        'rol': rol
    }
    guardar_usuarios()

def eliminar_usuario(nombre_usuario):
    """Elimina un usuario del archivo JSON."""
    global usuarios
    if nombre_usuario not in usuarios:
        raise ValueError("El usuario no existe.")
    
    del usuarios[nombre_usuario]
    guardar_usuarios()

def listar_usuarios():
    """Devuelve una lista de todos los usuarios."""
    global usuarios
    return usuarios

def agregar_compra(nombre_usuario, nombre_producto, cantidad):
    """Registra una compra de un producto por un usuario."""
    global compras, productos, carrito
    if nombre_usuario not in compras:
        compras[nombre_usuario] = []

    for producto in productos:
        if producto["nombre"] == nombre_producto:
            if producto["cantidad"] >= cantidad:
                compras[nombre_usuario].append({
                    "nombre": nombre_producto,
                    "precio": producto["precio"],
                    "cantidad": cantidad,
                    "total": producto["precio"] * cantidad
                })
                producto["cantidad"] -= cantidad
                carrito.append({
                    "nombre": nombre_producto,
                    "precio": producto["precio"],
                    "cantidad": cantidad,
                    "total": producto["precio"] * cantidad
                })
                guardar_productos()
                guardar_compras()
                return
            else:
                raise ValueError("Producto sin stock disponible.")
    raise ValueError("Producto no encontrado.")

def agregar_reposicion(nombre_producto, cantidad):
    """Registra un reporte de reposición de un producto."""
    global reposiciones
    if not nombre_producto or not cantidad:
        raise ValueError("Todos los campos son obligatorios.")
    
    try:
        cantidad = int(cantidad)
    except ValueError:
        raise ValueError("La cantidad debe ser un entero.")

    reposiciones.append({"nombre": nombre_producto, "cantidad": cantidad})
    guardar_reposiciones()

def listar_reposiciones():
    """Devuelve una lista de todos los reportes de reposición."""
    global reposiciones
    return reposiciones

def agregar_proveedor(nombre, telefono, producto):
    """Agrega un nuevo proveedor al archivo JSON."""
    global proveedores
    if not nombre or not telefono or not producto:
        raise ValueError("Todos los campos son obligatorios.")

    proveedores.append({"nombre": nombre, "telefono": telefono, "producto": producto})
    guardar_proveedores()

def eliminar_proveedor(nombre):
    """Elimina un proveedor del archivo JSON."""
    global proveedores
    if not nombre:
        raise ValueError("El nombre del proveedor es obligatorio.")

    for proveedor in proveedores:
        if proveedor["nombre"] == nombre:
            proveedores.remove(proveedor)
            guardar_proveedores()
            return
    raise ValueError("Proveedor no encontrado.")

def listar_proveedores():
    """Devuelve una lista de todos los proveedores."""
    global proveedores
    return proveedores

def limpiar_campos(*campos):
    """Limpia los campos de entrada."""
    for campo in campos:
        campo.delete(0, tk.END)

def iniciar_sesion():
    """Verifica las credenciales del usuario."""
    nombre_usuario = entrada_nombre_usuario.get().strip()
    contrasena = entrada_contrasena.get().strip()

    if nombre_usuario in usuarios and usuarios[nombre_usuario]['contrasena'] == contrasena:
        ventana_inicio.destroy()
        if usuarios[nombre_usuario]['rol'] == 'gerente':
            abrir_ventana_gerente()
        elif usuarios[nombre_usuario]['rol'] == 'empleado':
            abrir_ventana_empleado()
        else:
            abrir_ventana_cliente(nombre_usuario)
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

def abrir_ventana_gerente():
    """Abre la ventana principal del gerente."""
    global entrada_nombre_producto, entrada_precio, entrada_cantidad, area_texto, entrada_nombre_empleado, entrada_contrasena_empleado, entrada_eliminar_empleado
    global entrada_nombre_proveedor, entrada_telefono_proveedor, entrada_producto_proveedor, area_texto_proveedores, area_texto_reposiciones

    ventana = tk.Tk()
    ventana.title("Sistema de Tienda de Ortopedia - Gerente")
    ventana.configure(bg="lightblue")

    # Elementos de la GUI para productos
    etiqueta_nombre_producto = tk.Label(ventana, text="Nombre del Producto:", bg="lightblue")
    etiqueta_nombre_producto.grid(row=0, column=0, padx=10, pady=10)
    entrada_nombre_producto = tk.Entry(ventana)
    entrada_nombre_producto.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_precio = tk.Label(ventana, text="Precio:", bg="lightblue")
    etiqueta_precio.grid(row=1, column=0, padx=10, pady=10)
    entrada_precio = tk.Entry(ventana)
    entrada_precio.grid(row=1, column=1, padx=10, pady=10)

    etiqueta_cantidad = tk.Label(ventana, text="Cantidad:", bg="lightblue")
    etiqueta_cantidad.grid(row=2, column=0, padx=10, pady=10)
    entrada_cantidad = tk.Entry(ventana)
    entrada_cantidad.grid(row=2, column=1, padx=10, pady=10)

    boton_agregar_producto = tk.Button(ventana, text="Agregar Producto", command=lambda: manejar_accion_producto(agregar_producto))
    boton_agregar_producto.grid(row=3, column=0, padx=10, pady=10)
    boton_modificar_producto = tk.Button(ventana, text="Modificar Producto", command=lambda: manejar_accion_producto(modificar_producto))
    boton_modificar_producto.grid(row=3, column=1, padx=10, pady=10)
    boton_eliminar_producto = tk.Button(ventana, text="Eliminar Producto", command=lambda: manejar_accion_producto(eliminar_producto))
    boton_eliminar_producto.grid(row=4, column=0, padx=10, pady=10)
    boton_listar_productos = tk.Button(ventana, text="Listar Productos", command=listar_productos_gui)
    boton_listar_productos.grid(row=4, column=1, padx=10, pady=10)

    area_texto = tk.Text(ventana, height=10, width=50)
    area_texto.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Elementos de la GUI para empleados
    etiqueta_nombre_empleado = tk.Label(ventana, text="Nombre de Usuario del Empleado:", bg="lightblue")
    etiqueta_nombre_empleado.grid(row=6, column=0, padx=10, pady=10)
    entrada_nombre_empleado = tk.Entry(ventana)
    entrada_nombre_empleado.grid(row=6, column=1, padx=10, pady=10)

    etiqueta_contrasena_empleado = tk.Label(ventana, text="Contraseña del Empleado:", bg="lightblue")
    etiqueta_contrasena_empleado.grid(row=7, column=0, padx=10, pady=10)
    entrada_contrasena_empleado = tk.Entry(ventana)
    entrada_contrasena_empleado.grid(row=7, column=1, padx=10, pady=10)

    boton_agregar_usuario = tk.Button(ventana, text="Agregar Usuario", command=agregar_usuario_gui, bg="green", fg="white")
    boton_agregar_usuario.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    etiqueta_eliminar_empleado = tk.Label(ventana, text="Nombre de Usuario del Empleado a Eliminar:", bg="lightblue")
    etiqueta_eliminar_empleado.grid(row=9, column=0, padx=10, pady=10)
    entrada_eliminar_empleado = tk.Entry(ventana)
    entrada_eliminar_empleado.grid(row=9, column=1, padx=10, pady=10)

    boton_eliminar_usuario = tk.Button(ventana, text="Eliminar Empleado", command=eliminar_usuario_gui, bg="red", fg="white")
    boton_eliminar_usuario.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    boton_listar_usuarios = tk.Button(ventana, text="Listar Usuarios", command=listar_usuarios_gui, bg="blue", fg="white")
    boton_listar_usuarios.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    # Elementos de la GUI para ver reportes de reposición
    etiqueta_reposiciones = tk.Label(ventana, text="Reportes de Reposición:", bg="lightblue")
    etiqueta_reposiciones.grid(row=0, column=2, padx=10, pady=10)
    area_texto_reposiciones = tk.Text(ventana, height=10, width=50)
    area_texto_reposiciones.grid(row=1, column=2, rowspan=10, padx=10, pady=10)
    listar_reposiciones_gui(area_texto_reposiciones)

    # Elementos de la GUI para gestión de proveedores
    frame_proveedores = tk.Frame(ventana, bg="lightblue")
    frame_proveedores.grid(row=0, column=3, rowspan=14, padx=10, pady=10, sticky='ns')

    etiqueta_nombre_proveedor = tk.Label(frame_proveedores, text="Nombre del Proveedor:", bg="lightblue")
    etiqueta_nombre_proveedor.grid(row=0, column=0, padx=10, pady=10)
    entrada_nombre_proveedor = tk.Entry(frame_proveedores)
    entrada_nombre_proveedor.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_telefono_proveedor = tk.Label(frame_proveedores, text="Teléfono del Proveedor:", bg="lightblue")
    etiqueta_telefono_proveedor.grid(row=1, column=0, padx=10, pady=10)
    entrada_telefono_proveedor = tk.Entry(frame_proveedores)
    entrada_telefono_proveedor.grid(row=1, column=1, padx=10, pady=10)

    etiqueta_producto_proveedor = tk.Label(frame_proveedores, text="Producto que Provee:", bg="lightblue")
    etiqueta_producto_proveedor.grid(row=2, column=0, padx=10, pady=10)
    entrada_producto_proveedor = tk.Entry(frame_proveedores)
    entrada_producto_proveedor.grid(row=2, column=1, padx=10, pady=10)

    boton_agregar_proveedor = tk.Button(frame_proveedores, text="Agregar Proveedor", command=agregar_proveedor_gui, bg="green", fg="white")
    boton_agregar_proveedor.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    boton_eliminar_proveedor = tk.Button(frame_proveedores, text="Eliminar Proveedor", command=eliminar_proveedor_gui, bg="red", fg="white")
    boton_eliminar_proveedor.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    boton_listar_proveedores = tk.Button(frame_proveedores, text="Listar Proveedores", command=listar_proveedores_gui, bg="blue", fg="white")
    boton_listar_proveedores.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    area_texto_proveedores = tk.Text(frame_proveedores, height=10, width=50)
    area_texto_proveedores.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Botón para volver al login
    boton_volver = tk.Button(ventana, text="Volver", command=lambda: volver_al_login(ventana), bg="gray", fg="white")
    boton_volver.grid(row=14, column=0, columnspan=2, padx=10, pady=10)

    cargar_datos()
    ventana.mainloop()

def abrir_ventana_empleado():
    """Abre la ventana principal para empleados."""
    global entrada_nombre_producto, entrada_precio, entrada_cantidad, area_texto, entrada_producto_faltante, entrada_cantidad_faltante

    ventana = tk.Tk()
    ventana.title("Sistema de Tienda de Ortopedia - Empleado")
    ventana.configure(bg="lightyellow")

    # Elementos de la GUI para productos
    etiqueta_nombre_producto = tk.Label(ventana, text="Nombre del Producto:", bg="lightyellow")
    etiqueta_nombre_producto.grid(row=0, column=0, padx=10, pady=10)
    entrada_nombre_producto = tk.Entry(ventana)
    entrada_nombre_producto.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_precio = tk.Label(ventana, text="Precio:", bg="lightyellow")
    etiqueta_precio.grid(row=1, column=0, padx=10, pady=10)
    entrada_precio = tk.Entry(ventana)
    entrada_precio.grid(row=1, column=1, padx=10, pady=10)

    etiqueta_cantidad = tk.Label(ventana, text="Cantidad:", bg="lightyellow")
    etiqueta_cantidad.grid(row=2, column=0, padx=10, pady=10)
    entrada_cantidad = tk.Entry(ventana)
    entrada_cantidad.grid(row=2, column=1, padx=10, pady=10)

    boton_agregar = tk.Button(ventana, text="Agregar Producto", command=lambda: manejar_accion_producto(agregar_producto), bg="green", fg="white")
    boton_agregar.grid(row=3, column=0, padx=10, pady=10)

    boton_modificar = tk.Button(ventana, text="Modificar Producto", command=lambda: manejar_accion_producto(modificar_producto), bg="orange", fg="white")
    boton_modificar.grid(row=3, column=1, padx=10, pady=10)

    boton_eliminar = tk.Button(ventana, text="Eliminar Producto", command=lambda: manejar_accion_producto(eliminar_producto), bg="red", fg="white")
    boton_eliminar.grid(row=4, column=0, padx=10, pady=10)

    boton_listar = tk.Button(ventana, text="Listar Productos", command=listar_productos_gui, bg="blue", fg="white")
    boton_listar.grid(row=4, column=1, padx=10, pady=10)

    area_texto = tk.Text(ventana, height=10, width=50)
    area_texto.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Elementos para reporte de reposición
    etiqueta_producto_faltante = tk.Label(ventana, text="Producto Faltante:", bg="lightyellow")
    etiqueta_producto_faltante.grid(row=6, column=0, padx=10, pady=10)
    entrada_producto_faltante = tk.Entry(ventana)
    entrada_producto_faltante.grid(row=6, column=1, padx=10, pady=10)

    etiqueta_cantidad_faltante = tk.Label(ventana, text="Cantidad Necesaria:", bg="lightyellow")
    etiqueta_cantidad_faltante.grid(row=7, column=0, padx=10, pady=10)
    entrada_cantidad_faltante = tk.Entry(ventana)
    entrada_cantidad_faltante.grid(row=7, column=1, padx=10, pady=10)

    boton_reporte_reposicion = tk.Button(ventana, text="Generar Reporte de Reposición", command=generar_reporte_reposicion_gui, bg="purple", fg="white")
    boton_reporte_reposicion.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # Botón para volver al login
    boton_volver = tk.Button(ventana, text="Volver", command=lambda: volver_al_login(ventana), bg="gray", fg="white")
    boton_volver.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    cargar_datos()
    ventana.mainloop()

def abrir_ventana_cliente(nombre_usuario):
    """Abre la ventana principal para clientes."""
    global area_texto, entrada_compra_nombre, entrada_compra_cantidad

    ventana = tk.Tk()
    ventana.title("Sistema de Tienda de Ortopedia - Cliente")
    ventana.configure(bg="lightgreen")

    boton_listar = tk.Button(ventana, text="Listar Productos", command=listar_productos_gui, bg="blue", fg="white")
    boton_listar.grid(row=0, column=0, padx=10, pady=10)

    area_texto = tk.Text(ventana, height=10, width=50)
    area_texto.grid(row=1, column=0, padx=10, pady=10)

    etiqueta_compra_nombre = tk.Label(ventana, text="Nombre del Producto a Comprar:", bg="lightgreen")
    etiqueta_compra_nombre.grid(row=2, column=0, padx=10, pady=10)
    entrada_compra_nombre = tk.Entry(ventana)
    entrada_compra_nombre.grid(row=2, column=1, padx=10, pady=10)

    etiqueta_compra_cantidad = tk.Label(ventana, text="Cantidad a Comprar:", bg="lightgreen")
    etiqueta_compra_cantidad.grid(row=3, column=0, padx=10, pady=10)
    entrada_compra_cantidad = tk.Entry(ventana)
    entrada_compra_cantidad.grid(row=3, column=1, padx=10, pady=10)

    boton_comprar = tk.Button(ventana, text="Agregar al Carrito", command=lambda: manejar_compra(nombre_usuario), bg="purple", fg="white")
    boton_comprar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    boton_ver_carrito = tk.Button(ventana, text="Ver Carrito", command=ver_carrito, bg="orange", fg="white")
    boton_ver_carrito.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    boton_finalizar_compra = tk.Button(ventana, text="Finalizar Compra", command=finalizar_compra, bg="green", fg="white")
    boton_finalizar_compra.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Botón para volver al login
    boton_volver = tk.Button(ventana, text="Volver", command=lambda: volver_al_login(ventana), bg="gray", fg="white")
    boton_volver.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    cargar_datos()
    ventana.mainloop()

def ver_carrito():
    """Muestra el contenido del carrito y el total de la compra."""
    area_texto.delete(1.0, tk.END)
    total_compra = sum(item["total"] for item in carrito)
    for item in carrito:
        area_texto.insert(tk.END, f"Producto: {item['nombre']}, Cantidad: {item['cantidad']}, Precio Unitario: {item['precio']}, Total: {item['total']}\n")
    area_texto.insert(tk.END, f"\nTotal de la Compra: {total_compra}\n")

def finalizar_compra():
    """Permite al cliente seleccionar el método de pago y finaliza la compra."""
    def realizar_pago(metodo_pago):
        total_compra = sum(item["total"] for item in carrito)
        messagebox.showinfo("Compra Realizada", f"Su compra ha sido realizada con éxito.\nTotal: {total_compra}\nMétodo de Pago: {metodo_pago}")
        carrito.clear()
        ventana_pago.destroy()

    ventana_pago = tk.Toplevel()
    ventana_pago.title("Método de Pago")
    ventana_pago.configure(bg="lightgray")

    etiqueta_metodo_pago = tk.Label(ventana_pago, text="Seleccione el Método de Pago:", bg="lightgray")
    etiqueta_metodo_pago.grid(row=0, column=0, padx=10, pady=10)

    boton_efectivo = tk.Button(ventana_pago, text="Efectivo", command=lambda: realizar_pago("Efectivo"), bg="green", fg="white")
    boton_efectivo.grid(row=1, column=0, padx=10, pady=10)

    boton_tarjeta = tk.Button(ventana_pago, text="Tarjeta", command=lambda: realizar_pago("Tarjeta"), bg="blue", fg="white")
    boton_tarjeta.grid(row=1, column=1, padx=10, pady=10)

    boton_transferencia = tk.Button(ventana_pago, text="Transferencia", command=lambda: realizar_pago("Transferencia"), bg="purple", fg="white")
    boton_transferencia.grid(row=1, column=2, padx=10, pady=10)

def volver_al_login(ventana_actual):
    """Cierra la ventana actual y abre la ventana de login."""
    ventana_actual.destroy()
    abrir_ventana_login()

def manejar_accion_producto(accion):
    """Maneja las acciones de productos para agregar, modificar o eliminar."""
    nombre = entrada_nombre_producto.get().strip()
    precio = entrada_precio.get().strip()
    cantidad = entrada_cantidad.get().strip()
    try:
        accion(nombre, precio, cantidad)
        messagebox.showinfo("Éxito", f"Producto {accion.__name__.split('_')[0]} correctamente.")
        limpiar_campos(entrada_nombre_producto, entrada_precio, entrada_cantidad)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def listar_productos_gui():
    """Lista todos los productos en el área de texto."""
    area_texto.delete(1.0, tk.END)
    productos_listados = listar_productos()
    if not productos_listados:
        area_texto.insert(tk.END, "No hay productos registrados.\n")
    else:
        for producto in productos_listados:
            area_texto.insert(tk.END, f"Nombre: {producto['nombre']}, Precio: {producto['precio']}, Cantidad: {producto['cantidad']}\n")

def manejar_compra(nombre_usuario):
    """Maneja la compra de un producto por un cliente."""
    nombre_producto = entrada_compra_nombre.get().strip()
    cantidad = entrada_compra_cantidad.get().strip()

    try:
        cantidad = int(cantidad)
        agregar_compra(nombre_usuario, nombre_producto, cantidad)
        messagebox.showinfo("Éxito", f"Producto agregado al carrito correctamente.")
        limpiar_campos(entrada_compra_nombre, entrada_compra_cantidad)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ocurrió un error: {str(e)}")

def agregar_usuario_gui():
    """Agrega un nuevo usuario empleado al archivo JSON."""
    nombre_usuario = entrada_nombre_empleado.get().strip()
    contrasena = entrada_contrasena_empleado.get().strip()
    try:
        agregar_usuario(nombre_usuario, contrasena, rol='empleado')
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        limpiar_campos(entrada_nombre_empleado, entrada_contrasena_empleado)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def eliminar_usuario_gui():
    """Elimina un usuario empleado del archivo JSON."""
    nombre_usuario = entrada_eliminar_empleado.get().strip()
    try:
        eliminar_usuario(nombre_usuario)
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        limpiar_campos(entrada_eliminar_empleado)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def listar_usuarios_gui():
    """Lista todos los usuarios en el área de texto."""
    area_texto.delete(1.0, tk.END)
    usuarios_listados = listar_usuarios()
    if not usuarios_listados:
        area_texto.insert(tk.END, "No hay usuarios registrados.\n")
    else:
        for nombre_usuario, detalles in usuarios_listados.items():
            area_texto.insert(tk.END, f"Usuario: {nombre_usuario}, Rol: {detalles['rol']}\n")

def generar_reporte_reposicion_gui():
    """Genera un reporte de reposición."""
    nombre_producto = entrada_producto_faltante.get().strip()
    cantidad = entrada_cantidad_faltante.get().strip()

    try:
        agregar_reposicion(nombre_producto, cantidad)
        messagebox.showinfo("Éxito", f"Reporte de reposición generado correctamente.")
        limpiar_campos(entrada_producto_faltante, entrada_cantidad_faltante)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def listar_reposiciones_gui(area_texto_reposiciones):
    """Lista todos los reportes de reposición en el área de texto."""
    area_texto_reposiciones.delete(1.0, tk.END)
    reposiciones_listadas = listar_reposiciones()
    if not reposiciones_listadas:
        area_texto_reposiciones.insert(tk.END, "No hay reportes de reposición.\n")
    else:
        for reposicion in reposiciones_listadas:
            area_texto_reposiciones.insert(tk.END, f"Producto: {reposicion['nombre']}, Cantidad Necesaria: {reposicion['cantidad']}\n")

def agregar_proveedor_gui():
    """Agrega un nuevo proveedor al archivo JSON."""
    nombre_proveedor = entrada_nombre_proveedor.get().strip()
    telefono_proveedor = entrada_telefono_proveedor.get().strip()
    producto_proveedor = entrada_producto_proveedor.get().strip()
    try:
        agregar_proveedor(nombre_proveedor, telefono_proveedor, producto_proveedor)
        messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
        limpiar_campos(entrada_nombre_proveedor, entrada_telefono_proveedor, entrada_producto_proveedor)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def eliminar_proveedor_gui():
    """Elimina un proveedor del archivo JSON."""
    nombre_proveedor = entrada_nombre_proveedor.get().strip()
    try:
        eliminar_proveedor(nombre_proveedor)
        messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        limpiar_campos(entrada_nombre_proveedor)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def listar_proveedores_gui():
    """Lista todos los proveedores en el área de texto."""
    area_texto_proveedores.delete(1.0, tk.END)
    proveedores_listados = listar_proveedores()
    if not proveedores_listados:
        area_texto_proveedores.insert(tk.END, "No hay proveedores registrados.\n")
    else:
        for proveedor in proveedores_listados:
            area_texto_proveedores.insert(tk.END, f"Nombre: {proveedor['nombre']}, Teléfono: {proveedor['telefono']}, Producto: {proveedor['producto']}\n")

def abrir_ventana_registro(rol):
    """Abre la ventana de registro para nuevos usuarios."""
    global entrada_registro_usuario, entrada_registro_contrasena, ventana_registro

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro")
    ventana_registro.configure(bg="lightgray")

    etiqueta_registro_usuario = tk.Label(ventana_registro, text="Nombre de Usuario:", bg="lightgray")
    etiqueta_registro_usuario.grid(row=0, column=0, padx=10, pady=10)
    entrada_registro_usuario = tk.Entry(ventana_registro)
    entrada_registro_usuario.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_registro_contrasena = tk.Label(ventana_registro, text="Contraseña:", bg="lightgray")
    etiqueta_registro_contrasena.grid(row=1, column=0, padx=10, pady=10)
    entrada_registro_contrasena = tk.Entry(ventana_registro, show="*")
    entrada_registro_contrasena.grid(row=1, column=1, padx=10, pady=10)

    boton_registro = tk.Button(ventana_registro, text="Registrar", command=lambda: manejar_registro(rol), bg="blue", fg="white")
    boton_registro.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def manejar_registro(rol):
    """Maneja el registro de nuevos usuarios."""
    nombre_usuario = entrada_registro_usuario.get().strip()
    contrasena = entrada_registro_contrasena.get().strip()
    try:
        agregar_usuario(nombre_usuario, contrasena, rol)
        messagebox.showinfo("Éxito", "Registro completado correctamente.")
        ventana_registro.destroy()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def abrir_ventana_login():
    """Abre la ventana de login."""
    global ventana_inicio, entrada_nombre_usuario, entrada_contrasena

    ventana_inicio = tk.Tk()
    ventana_inicio.title("Inicio de Sesión")
    ventana_inicio.configure(bg="lightgray")

    etiqueta_nombre_usuario = tk.Label(ventana_inicio, text="Nombre de Usuario:", bg="lightgray")
    etiqueta_nombre_usuario.grid(row=0, column=0, padx=10, pady=10)
    entrada_nombre_usuario = tk.Entry(ventana_inicio)
    entrada_nombre_usuario.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_contrasena = tk.Label(ventana_inicio, text="Contraseña:", bg="lightgray")
    etiqueta_contrasena.grid(row=1, column=0, padx=10, pady=10)
    entrada_contrasena = tk.Entry(ventana_inicio, show="*")
    entrada_contrasena.grid(row=1, column=1, padx=10, pady=10)

    boton_iniciar_sesion = tk.Button(ventana_inicio, text="Iniciar Sesión", command=iniciar_sesion, bg="blue", fg="white")
    boton_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    boton_registrarse = tk.Button(ventana_inicio, text="Registrarse", command=lambda: abrir_ventana_registro('cliente'), bg="green", fg="white")
    boton_registrarse.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    cargar_datos()
    ventana_inicio.mainloop()

# Iniciar el programa abriendo la ventana de inicio de sesión
abrir_ventana_login()
