from flask import Flask, jsonify
import requests
import logging
from functools import partial

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

URL_CATALOGO = "http://ms-catalogo:5001/producto"

URL_PAGOS = "http://ms-pagos:5002/pagos/transaccion"
URL_PAGOS_COMP = "http://ms-pagos:5002/pagos/compensar"

URL_INV = "http://ms-inventario:5003/inventario"

URL_COMPRAS = "http://ms-compras:8080/compras/realizar"
URL_COMPRAS_COMP = "http://ms-compras:8080/compras/compensar"

def nombrar(func, nombre):
    func.__name__ = nombre
    return func


# --------------------------- SAGA ---------------------------
class Saga:
    def __init__(self, data):
        self.data = data
        self.pasos = []
        self.compensaciones = []

    def agregar(self, accion, compensacion=None):
        # Siempre se guarda la tupla (acción, compensación)
        self.pasos.append((accion, compensacion))

    def ejecutar(self):
        for accion, compensacion in self.pasos:

            status = accion()
            logging.info(f"Paso ejecutado: {accion.__name__} | status = {status}")

            if status != 200:
                logging.error(f"Paso fallido: {accion.__name__}")
                self.revertir()
                return jsonify({
                    "status": "failed",
                    "error": accion.__name__
                }), 409

            # SOLO agregamos compensaciones de pasos exitosos
            if compensacion:
                self.compensaciones.append(compensacion)

        return jsonify({"status": "success", "producto": self.data}), 200

    def revertir(self):
        logging.info("=== INICIANDO COMPENSACIONES ===")

        for compensacion in reversed(self.compensaciones):
            logging.info(f"Ejecutando compensación → {compensacion.__name__}")

            try:
                respuesta = compensacion()
                logging.info(f"Compensación {compensacion.__name__} ejecutada correctamente")
            except Exception as e:
                logging.error(f"Error ejecutando compensación {compensacion.__name__}: {e}")

        logging.info("=== FIN COMPENSACIONES ===")




# ---------------------- PASOS ----------------------
def obtener_producto():
    r = requests.get(URL_CATALOGO)
    return r.json()["producto"]

def paso_inventario(producto):
    return requests.get(URL_INV).status_code

def paso_pago(producto):
    return requests.post(URL_PAGOS, json=producto).status_code

def compensar_pago():
    requests.post(URL_PAGOS_COMP)

def paso_registrar(producto):
    return requests.post(URL_COMPRAS, json=producto).status_code

def compensar_registrar(producto):
    requests.post(URL_COMPRAS_COMP, json=producto)


# -------------------- ENDPOINT ---------------------
@app.route("/orquestar/compra", methods=["POST"])
def orquestar_compra():
    producto = obtener_producto()
    logging.info(f"Producto obtenido: {producto}")

    saga = Saga(producto)

    # Paso 1 - inventario (SIN compensación)
    saga.agregar(
        nombrar(partial(paso_inventario, producto), "paso_inventario"),
        None
    )

    # Paso 2 - pago
    saga.agregar(
        nombrar(partial(paso_pago, producto), "paso_pago"),
        nombrar(compensar_pago, "compensar_pago")
    )

    # Paso 3 - registrar compra
    saga.agregar(
        nombrar(partial(paso_registrar, producto), "paso_registrar"),
        nombrar(partial(compensar_registrar, producto), "compensar_registrar")
    )

    return saga.ejecutar()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
