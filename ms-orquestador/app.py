from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ======================
#  URLs (Docker Compose)
# ======================

URL_CATALOGO = "http://ms-catalogo:5001/catalogo/producto"

URL_PAGOS = "http://ms-pagos:5002/pagos/transaccion"
URL_PAGOS_COMP = "http://ms-pagos:5002/pagos/compensar"

URL_INV = "http://ms-inventario:5003/inventario/reservar"
URL_INV_COMP = "http://ms-inventario:5003/inventario/compensar"

URL_COMPRAS = "http://ms-compras:8080/compras/realizar"
URL_COMPRAS_COMP = "http://ms-compras:8080/compras/compensar"


# ======================
#   SAGA ORQUESTADOR
# ======================

class Saga:
    def __init__(self, data):
        self.data = data
        self.steps = []
        self.compensations = []

    def add(self, action, compensation):
        self.steps.append(action)
        self.compensations.insert(0, compensation)

    def run(self):
        for step in self.steps:
            status = step()
            if status != 200:
                self.rollback()
                return jsonify({"status": "failed", "error": step.__name__}), 409

        return jsonify({"status": "success", "producto": self.data}), 200

    def rollback(self):
        for c in self.compensations:
            c()


# ======================
#   Servicios
# ======================

def get_producto():
    r = requests.get(URL_CATALOGO)
    return r.json()["producto"]

def pagar(prod):
    return requests.post(URL_PAGOS, json=prod).status_code

def pagar_comp():
    requests.post(URL_PAGOS_COMP)

def reservar_inv(prod):
    return requests.post(URL_INV, json=prod).status_code

def reservar_inv_comp():
    requests.post(URL_INV_COMP)

def registrar_compra(prod):
    return requests.post(URL_COMPRAS, json=prod).status_code

def registrar_compra_comp():
    requests.post(URL_COMPRAS_COMP)


# ======================
#   Endpoint principal
# ======================

@app.route("/orquestar/compra", methods=["POST"])
def ejecutar_saga():

    producto = get_producto()

    saga = Saga(producto)

    saga.add(lambda: pagar(producto), pagar_comp)
    saga.add(lambda: reservar_inv(producto), reservar_inv_comp)
    saga.add(lambda: registrar_compra(producto), registrar_compra_comp)

    return saga.run()


@app.route("/")
def home():
    return {"mensaje": "Orquestador funcionando"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
