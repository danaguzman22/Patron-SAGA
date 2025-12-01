from flask import Flask, jsonify
import requests
import logging

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

class Saga:
    def __init__(self, data):
        self.data = data
        self.pasos = []
        self.compensaciones = []

    def agregar(self, accion, compensacion=None):
        
        self.pasos.append(accion)
        if compensacion:
            self.compensaciones.insert(0, compensacion)

    def ejecutar(self):
        for paso in self.pasos:
            status = paso()
            logging.info(f"Paso ejecutado: {paso.__name__} | status = {status}")

            if status != 200:
                logging.error(f"Paso fallido: {paso.__name__}")
                self.revertir()

                return jsonify({
                    "status": "failed",
                    "error": paso.__name__
                }), 409

        return jsonify({
            "status": "success",
            "producto": self.data
        }), 200

    def revertir(self):
        logging.info("Ejecutando compensaciones...")
        for compensacion in self.compensaciones:
            logging.info(f"Compensación: {compensacion.__name__}")
            compensacion()


def obtener_producto():
    r = requests.get(URL_CATALOGO)
    return r.json()["producto"]

# --- INVENTARIO ---
def paso_inventario(producto):
    return requests.get(URL_INV).status_code

# --- PAGO ---
def paso_pago(producto):
    return requests.post(URL_PAGOS, json=producto).status_code

def compensar_pago():
    requests.post(URL_PAGOS_COMP)


# --- REGISTRAR COMPRA ---
def paso_registrar(producto):
    return requests.post(URL_COMPRAS, json=producto).status_code

def compensar_registrar(producto):
    requests.post(URL_COMPRAS_COMP, json=producto)


@app.route("/orquestar/compra", methods=["POST"])
def orquestar_compra():
    producto = obtener_producto()
    logging.info(f"Producto obtenido: {producto}")

    saga = Saga(producto)

    saga.agregar(lambda: paso_inventario(producto))

    saga.agregar(lambda: paso_pago(producto), compensar_pago)

    saga.agregar(lambda: paso_registrar(producto),
                 lambda: compensar_registrar(producto))

    return saga.ejecutar()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5010)