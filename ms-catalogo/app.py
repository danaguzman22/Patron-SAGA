from flask import Flask, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)  # Permite peticiones desde otros microservicios

# Simulación de productos disponibles
productos = [
    {"id": 1, "nombre": "Auriculares Bluetooth", "precio": 25000, "stock": 15},
    {"id": 2, "nombre": "Teclado Mecánico", "precio": 40000, "stock": 10},
    {"id": 3, "nombre": "Mouse Gamer", "precio": 18000, "stock": 20},
    {"id": 4, "nombre": "Monitor 24''", "precio": 95000, "stock": 5},
    {"id": 5, "nombre": "Silla Ergonómica", "precio": 120000, "stock": 8},
]

@app.route("/producto", methods=["GET"])
def obtener_producto():
    """
    Endpoint que retorna un producto aleatorio (status 200)
    Simula una pequeña latencia de red (entre 0.5 y 2 segundos)
    """

    # Simular latencia de red
    time.sleep(random.uniform(0.5, 2.0))

    # Elegir producto aleatorio
    producto = random.choice(productos)

    # Crear nuevo diccionario SIN el campo 'stock'
    producto_sin_stock = {
        "id": producto["id"],
        "nombre": producto["nombre"],
        "precio": producto["precio"]
    }

    # Log de lo que se devuelve
    print(f"[CATÁLOGO] Producto devuelto: {producto['nombre']} (ID {producto['id']})")

    # Retornar respuesta en formato JSON sin el stock
    return jsonify({
        "status": 200,
        "mensaje": "Producto obtenido con éxito",
        "producto": producto_sin_stock
    }), 200

if __name__ == "__main__":
    # Ejecutar el microservicio
    app.run(host="0.0.0.0", port=5001, debug=True)
