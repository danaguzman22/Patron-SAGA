from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ==========================
#  URLs de los microservicios
# ==========================

URL_CATALOGO = "http://ms-catalogo:5001/producto"

URL_PAGOS = "http://ms-pagos:5002/pagos/transaccion"
URL_PAGOS_COMP = "http://ms-pagos:5002/pagos/compensar"

URL_INV = "http://ms-inventario:5003/inventario/reservar"
URL_INV_COMP = "http://ms-inventario:5003/inventario/compensar"

URL_COMPRAS = "http://ms-compras:8080/compras/realizar"
URL_COMPRAS_COMP = "http://ms-compras:8080/compras/compensar"


# ==========================
#   Clase Saga
# ==========================

class Saga:
    def __init__(self, data):
        self.data = data
        self.pasos = []
        self.compensaciones = []

    def agregar(self, accion, compensacion):
        self.pasos.append(accion)
        self.compensaciones.insert(0, compensacion)

    def ejecutar(self):
        for paso in self.pasos:
            status = paso()
            if status != 200:           # si falla uno, se invierten las compensaciones
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
        for compensacion in self.compensaciones:
            compensacion()


# ==========================
#   Funciones de microservicios
# ==========================

def obtener_producto():
    r = requests.get(URL_CATALOGO)
    return r.json()["producto"]

def pagar(producto):
    return requests.post(URL_PAGOS, json=producto).status_code

def pagar_comp():
    requests.post(URL_PAGOS_COMP)

def inventario(producto):
    return requests.post(URL_INV, json=producto).status_code

def inventario_comp():
    requests.post(URL_INV_COMP)

def registrar_compra(producto):
    return requests.post(URL_COMPRAS, json=producto).status_code

def registrar_compra_comp():
    requests.post(URL_COMPRAS_COMP)


# ==========================
#      Endpoint principal
# ==========================

@app.route("/orquestar/compra", methods=["POST"])
def orquestar_compra():

    producto = obtener_producto()

    saga = Saga(producto)

    saga.agregar(lambda: pagar(producto), pagar_comp)
    saga.agregar(lambda: inventario(producto), inventario_comp)
    saga.agregar(lambda: registrar_compra(producto), registrar_compra_comp)

    return saga.ejecutar()


@app.route("/")
def home():
    return {"mensaje": "Orquestador funcionando"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
