from flask import Flask
from config import Config
from extensions import db, mail, socketio
from routes.user_routes import user_bp
from routes.message_routes import message_bp
from routes.skill_routes import skill_bp
from routes.notification_routes import notification_bp
from routes.review_routes import review_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail.init_app(app)
socketio.init_app(app)



app.register_blueprint(user_bp, url_prefix='/auth')
app.register_blueprint(message_bp, url_prefix='/messages')
app.register_blueprint(skill_bp, url_prefix='/skills')
app.register_blueprint(notification_bp, url_prefix='/notifications')
app.register_blueprint(review_bp, url_prefix='/reviews')


with app.app_context():
    db.create_all()  # Create tables

if __name__ == '__main__':
    socketio.run(app, debug=True)
