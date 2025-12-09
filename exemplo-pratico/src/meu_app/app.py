from flask import Flask
from config import Config
from models.produto_model import db
from routes.produto_routes import produto_bp
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Inicializar Swagger
swagger = Swagger(app)

# Blueprints
app.register_blueprint(produto_bp)

@app.route("/status")
def status():
    """
    Verifica o status da API
    ---
    tags:
      - Status
    responses:
      200:
        description: API funcionando
    """
    return {"status": "ok", "version": "1.0.0"}, 200

if __name__ == "__main__":
    app.run(debug=True)
