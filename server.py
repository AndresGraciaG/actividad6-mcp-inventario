from mcp.server.fastmcp import FastMCP
import sqlite3
from database import init_db, DB_NAME


init_db()

mcp = FastMCP("InventarioDB")

def get_connection():
    return sqlite3.connect(DB_NAME)

                                                            #! Herramientas para gestionar el inventario

#? Método para crear un nuevo producto.
@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float)-> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
        (nombre, categoria, cantidad, precio)
    )
    conn.commit()
    conn.close()

    return "Producto creado exitosamente"

#? Método para consultar un producto existente.
@mcp.tool()
def consultar_producto(id: int)-> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
        "id": row[0],
        "nombre": row[1],
        "categoria": row[2],
        "cantidad": row[3],
        "precio": row[4]
        }

    return {"error": "Producto no encontrado"}


#? Método para actualizar la cantidad de un producto.
@mcp.tool()
def actualizar_producto(id: int, cantidad: int)-> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "UPDATE productos SET cantidad = ? WHERE id = ?",
    (cantidad, id)
    )

    conn.commit()
    conn.close()

    return "Producto actualizado correctamente"

#? Método para eliminar un producto del inventario.
@mcp.tool()
def eliminar_producto(id: int)-> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return "Producto eliminado correctamente"


#? Método para listar todos los productos en el inventario.
@mcp.tool()
def listar_productos()-> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()

    conn.close()

    return [
    {
    "id": row[0],
    "nombre": row[1],
    "categoria": row[2],
    "cantidad": row[3],
    "precio": row[4]
    }
    for row in rows
    ]
    
    
#? Método para calcular el valor total del inventario.
@mcp.tool()
def calcular_valor_total_inventario()-> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
    total = cursor.fetchone()[0]

    conn.close()

    return {"valor_total_inventario": total if total else 0}

#? Método para listar productos agotados (cantidad = 0).
@mcp.tool()
def productos_agotados()-> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad = 0")
    rows = cursor.fetchall()

    conn.close()

    return [
    {
    "id": row[0],
    "nombre": row[1],
    "categoria": row[2],
    "cantidad": row[3],
    "precio": row[4]
    }
    for row in rows
    ]

#? Método para encontrar el producto más costoso en el inventario.    
@mcp.tool()
def producto_mas_costoso()-> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
        "id": row[0],
        "nombre": row[1],
        "categoria": row[2],
        "cantidad": row[3],
        "precio": row[4]
        }

    return {"error": "No hay productos registrados"}


#? Método para obtener estadísticas generales del inventario (total de productos, promedio de cantidad, promedio de precio, valor total).
@mcp.tool()
def estadisticas_inventario()-> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*), AVG(cantidad), AVG(precio), SUM(cantidad * precio) FROM productos")

    total_productos, promedio_cantidad, promedio_precio, valor_total = cursor.fetchone()
    
    conn.close()

    return {
    "total_productos": total_productos,
    "promedio_cantidad": promedio_cantidad,
    "promedio_precio": promedio_precio,
    "valor_total": valor_total if valor_total else 0
    }
    
    
# # Recursos MCP para consultar datos del inventario
# @mcp.resource("inventario://productos")
# def recurso_listar_productos() -> list:
#     """Lista todos los productos del inventario."""
#     return listar_productos()


# @mcp.resource("inventario://productos/{id}")
# def recurso_consultar_producto(id: str) -> dict:
#     """Consulta un producto por ID."""
#     return consultar_producto(int(id))


# @mcp.resource("inventario://valor-total")
# def recurso_valor_total_inventario() -> dict:
#     """Calcula el valor total del inventario."""
#     return calcular_valor_total_inventario()


# @mcp.resource("inventario://productos-agotados")
# def recurso_productos_agotados() -> list:
#     """Lista los productos agotados."""
#     return productos_agotados()


# @mcp.resource("inventario://producto-mas-costoso")
# def recurso_producto_mas_costoso() -> dict:
#     """Devuelve el producto más costoso del inventario."""
#     return producto_mas_costoso()


# @mcp.resource("inventario://estadisticas")
# def recurso_estadisticas_inventario() -> dict:
#     """Devuelve estadísticas generales del inventario."""
#     return estadisticas_inventario()
    
if __name__ == "__main__":
    print("Iniciando MCP...")
    mcp.run()