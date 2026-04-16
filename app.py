from flask import Flask
from config import Config
from extentions import mail
from views import views_bp
from auth import auth_bp
from admin import admin_bp


app = Flask(__name__)
app.config.from_object(Config)

mail.init_app(app)

app.register_blueprint(views_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


if __name__ == '__main__':
    app.run(debug = True)