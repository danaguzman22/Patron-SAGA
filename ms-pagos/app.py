from flask import Flask
from blueprints.pagos import pagos_bp


app = Flask(__name__)
app.register_blueprint(pagos_bp, url_prefix="/pagos")

if __name__ == "__main__":
    app.run(port=5002, debug=True)
