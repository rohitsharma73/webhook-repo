from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb+srv://rohitsharma93686:A4MYFpzhfsjtznEb@cluster0.vqdc1to.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    mongo.init_app(app)
    app.register_blueprint(webhook)
    
    return app
