from flask import Blueprint, jsonify
import random

pagos_bp = Blueprint("pagos", __name__)


@pagos_bp.route("/transaccion", methods=["POST"])
def procesar_pago():
    status = random.choice([200, 409])
    if status == 200:
        return jsonify({"mensaje": "Pago realizado correctamente"}), 200
    else:
        return jsonify({"mensaje": "Error en el pago (conflicto)"}), 409

@pagos_bp.route("/compensar", methods=["POST"])
def compensar_pago():
    return jsonify({"mensaje": "Pago compensado correctamente"}), 200

