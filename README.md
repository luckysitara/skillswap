# skillswap

venom@venom-Precision-5520:~/skillswap$ cat */*
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({'error': 'Invalid email or password'}), 401
cat: auth/__pycache__: Is a directory
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import User
from extensions import db

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201
from flask import Blueprint, render_template, request, redirect, url_for, flash

from .forms import LoginForm, SignupForm
from models import User, db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Password check should be hashed
            return redirect(url_for('some_protected_route'))  # Change as necessary
        flash('Login failed. Check your email and password.')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)  # Password should be hashed
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')
from flask import Blueprint
from .views import send_message, view_messages

messages = Blueprint('messages', __name__)

# Routes for messaging
messages.add_url_rule('/messages', 'view_messages', view_messages, methods=['GET'])
messages.add_url_rule('/messages', 'send_message', send_message, methods=['POST'])

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Message, User
from extensions import db

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender_id = get_jwt_identity()
    recipient_id = data.get('recipient_id')
    content = data.get('content')

    new_message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
    
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 201

@message_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    user_id = get_jwt_identity()
    messages = Message.query.filter((Message.sender_id == user_id) | (Message.recipient_id == user_id)).all()
    return jsonify([{
        'sender': User.query.get(message.sender_id).username,
        'recipient': User.query.get(message.recipient_id).username,
        'content': message.content,
        'timestamp': message.timestamp
    } for message in messages]), 200
cat: messages/__pycache__: Is a directory
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
#from models import db, Message, User
from datetime import datetime




message_routes_bp = Blueprint('messages', __name__)
# View Messages (GET)
@message_routes_bp.route('/')
def view_messages():
    if 'user_id' not in session:
        flash('You need to log in to view your messages', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    received_messages = Message.query.filter_by(recipient_id=user_id).all()
    sent_messages = Message.query.filter_by(sender_id=user_id).all()

    return render_template('messages.html', received_messages=received_messages, sent_messages=sent_messages)

# Send a message (POST)
def send_message():
    if 'user_id' not in session:
        flash('You need to log in to send a message', 'danger')
        return redirect(url_for('auth.login'))

    sender_id = session['user_id']
    recipient_email = request.form.get('recipient_email')
    content = request.form.get('content')

    # Find recipient user by email
    recipient = User.query.filter_by(email=recipient_email).first()

    if not recipient:
        flash('Recipient not found!', 'danger')
        return redirect(url_for('messages.view_messages'))

    # Create new message
    new_message = Message(
        sender_id=sender_id,
        recipient_id=recipient.id,
        content=content,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_message)
    db.session.commit()

    flash('Message sent successfully!', 'success')
    return redirect(url_for('messages.view_messages'))
flask db init
flask db migrate
flask db upgrade
from flask import Blueprint

proposal_routes_bp = Blueprint('proposals', __name__)

from .proposal_routes import create_proposal  # Import routes last to avoid circular imports
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Proposal, Skill
from extensions import db

proposal_bp = Blueprint('proposal_bp', __name__)

@proposal_bp.route('/proposals', methods=['POST'])
@jwt_required()
def create_proposal():
    data = request.get_json()
    offer_skill_id = data.get('offer_skill_id')
    request_skill_id = data.get('request_skill_id')

    new_proposal = Proposal(offer_skill_id=offer_skill_id, request_skill_id=request_skill_id)

    db.session.add(new_proposal)
    db.session.commit()

    return jsonify({'message': 'Proposal created successfully'}), 201

@proposal_bp.route('/proposals', methods=['GET'])
@jwt_required()
def get_proposals():
    user_id = get_jwt_identity()
    proposals = Proposal.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'offer_skill_id': proposal.offer_skill_id,
        'request_skill_id': proposal.request_skill_id,
        'status': proposal.status
    } for proposal in proposals]), 200
cat: proposals/__pycache__: Is a directory
�
���f����ddlmZddlmZddlmZddlmZddm	Z	ddl
m
 Z
  ddl
ee�Zej j#�ej$e�ej'ed	�
�ej'ed
      �
�ej'e	d
         �
�ej'ed
d�j'e
�ddlmZedk(rej-d��yy)�)�Flask)�db)�auth_bp)�message_routes_bp)�proposal_routes_bp)�	rating_bp)�skill_routes_bp�configz/auth)�
url_prefixz	/messagesz
/proposals/ratingsz/skills)�views__main__T)�debugN)�flaskr�modelsr�authr�messages.viewsr�	proposalsr�ratings.rating_routes�skillsr	__name__�appr
�
 from_objectinit_app�register_blueprint�rating_routes_bpr
                                                         �run���/home/venom/skillswap/app.py<module>r s������,�(�+�"�
                                     �H�o���
�
���x� �
       ��
         �
          �C�����w�7��3����(�[��A����)�l��C����'�J��?�����9��=�
                                                               �z���G�G�$�G���r�
�r�f���R�ddlmZddlmZddlmZe�Ze�Ze�y)�)�
SQLAlchemy)�
flask_migrater�db�jwt�migrate���#/home/venom/skillswap/extensions.py<module>rs#��'�)�!��\���l��
�)�r
���f�����ddlmZddlmZe�ZGd�de�ZGd�de�ZGd�e�ZGd	�d
e�Gd
    �d
)�)datetime)�	y
SQLAlchemyc��eZdZej	ej
d��Zej	ejd�dd��ej	ejd�dd��Z	ej	ejd�d�Z
y	)
�UserT��
        primary_key�PF)�uniquenullable�x��r
                                           N)
                                             __name__�
__module__�
           __qualname__�db�Column�Integer�id�Stringusername�emailpassword���/home/venom/skillswap/models.pyrrsj��	
                                        ���2�:�:�4��	0�B��y�y����2��t�e�y�D�H�
 �I�I�b�i�i��n�T�E�I�
                     B�E��y�y����3��%�y�8�Hrc�$�eZdZej	ej
d��Zej	ejd�d��ej	ejd�d��Z	ej	ej
ejd��Z
      y�SkillTrr	Fr�user.idN)
                                    rrrrrrrr�
skill_namecategory�
ForeignKey�user_idr�rrr
                       si��	
                                ���2�:�:�4��	0�B����2�9�9�R�=�5��9�J��y�y����2���y�7�H��i�i��
�
�B�M�M�)�$<�=�Grc��eZdZej	ej
d��Zej	ej
ejd�d��ej	ej
ejd�d��Z	ej	ej
d��Z
ej	ej�Z
            ejg��Zeje	g��Z)	�RatingTrrFrr��
                                               foreign_keysN)rrrrrrrr"rater_idrated_id�rating�Text�comment�
                           relationship�rater�ratedr�rr%r%s���	
                                                                ���2�:�:�4��	0�O�O�F�(���O��G��]�9�%=��y�N�H��y�y������R�]�]�9�%=��y�N�H�
             <�E�
                 �O�O�F�(���O�
                              <�Er%c���eZdZej	ej
d��Zej	ej
ejd�d��ej	ej
ejd�d��Z	ej	ejd��Z
jd��Zej!dg�Zej!de       g�Zy  ej)	eje
�MessageTrrFr)�defaultr
                       rr&N)rrrrrrrr"�	sender_id�
                                                  recipient_idr+�contentDateTimer�utcnow�	timestampr-�sender�	recipientr�rr1r1s���	
                                                                ���2�:�:�4��	0�B��	�	�"�*�*�b�m�m�I�&>��	�O�I��9�9�R�Z�Z����y�)A�E�9�R�L��i�i����>�F�����l�^��D�Ir1c�>�eZdZej�+�xej��	�O�I�
d��Zej	ej
ejd�d��ej	ej
ejd�d��Z	ej	ejd�d�Z
                               y	)
ProposalTrskill.idFr�2�pending)r2N)
                                   rrrrrrrr"�offer_skill_id�request_skill_idr�statusr�rr<r<*sv��	
                        ���2�:�:�4��	0�B��Y�Y�r�z�z�2�=�=���+D�u�Y�U�N��y�y��8�Fr<N)y�y��}�i�Y�y�W��
r�flask_sqlalchemyrr�Modelrrr%r1r<r�r<module>rDsd���'��\��9�2�8�8�9�
                                                                    >�B�H�H�>�	=�R�X�X�	=E�b�h�hE�9�r�x�x�9rrom flask import Blueprint
from .views import rate_user, view_ratings

ratings = Blueprint('ratings', __name__)

# Routes for ratings
ratings.add_url_rule('/rate/<int:user_id>', 'rate_user', rate_user, methods=['POST'])
ratings.add_url_rule('/ratings', 'view_ratings', view_ratings, methods=['GET'])
cat: ratings/__pycache__: Is a directory
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Rating
from extensions import db

rating_bp = Blueprint('rating_bp', __name__)

@rating_bp.route('/ratings', methods=['POST'])
@jwt_required()
def create_rating():
    data = request.get_json()
    user_id = data.get('user_id')
    partner_id = data.get('partner_id')
    rating = data.get('rating')
    review = data.get('review')

    new_rating = Rating(user_id=user_id, partner_id=partner_id, rating=rating, review=review)
    
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({'message': 'Rating submitted successfully'}), 201
from flask import request, redirect, url_for, flash, session, render_template
from models import db, User, Rating
from sqlalchemy import func

# Rate a user (POST)
def rate_user(user_id):
    if 'user_id' not in session:
        flash('You need to log in to rate a user', 'danger')
        return redirect(url_for('auth.login'))

    rater_id = session['user_id']
    rating_value = int(request.form.get('rating'))
    comment = request.form.get('comment')

    # Ensure rating is between 1 and 5
    if rating_value < 1 or rating_value > 5:
        flash('Rating must be between 1 and 5 stars', 'danger')
        return redirect(url_for('users.profile', user_id=user_id))

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('main.index'))

    # Check if the rater has already rated this user
    existing_rating = Rating.query.filter_by(rater_id=rater_id, rated_id=user_id).first()
    if existing_rating:
        flash('You have already rated this user', 'info')
        return redirect(url_for('users.profile', user_id=user_id))

    # Create new rating
    new_rating = Rating(
        rater_id=rater_id,
        rated_id=user_id,
        rating=rating_value,
        comment=comment
    )

    db.session.add(new_rating)
    db.session.commit()

    flash('Rating submitted successfully!', 'success')
    return redirect(url_for('users.profile', user_id=user_id))

# View user ratings (GET)
def view_ratings():
    if 'user_id' not in session:
        flash('You need to log in to view ratings', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_ratings = Rating.query.filter_by(rated_id=user_id).all()
    
    # Calculate average rating
    average_rating = db.session.query(func.avg(Rating.rating)).filter_by(rated_id=user_id).scalar()

    return render_template('ratings.html', ratings=user_ratings, average_rating=average_rating)
cat: skap/bin: Is a directory
cat: skap/include: Is a directory
cat: skap/lib: Is a directory
cat: skap/lib64: Is a directory
home = /usr/bin
include-system-site-packages = false
version = 3.12.3
executable = /usr/bin/python3.12
command = /usr/bin/python3 -m venv /home/venom/skillswap/skap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField('Skill Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')
from flask import Blueprint
from .views import add_skill, edit_skill, view_skills

skills = Blueprint('skills', __name__)

# Routes for skills management
skills.add_url_rule('/skills', 'view_skills', view_skills, methods=['GET'])
skills.add_url_rule('/skills/add', 'add_skill', add_skill, methods=['GET', 'POST'])
skills.add_url_rule('/skills/edit/<int:skill_id>', 'edit_skill', edit_skill, methods=['GET', 'POST'])
cat: skills/__pycache__: Is a directory
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Skill, User
from extensions import db

skill_bp = Blueprint('skill_bp', __name__)

@skill_bp.route('/skills', methods=['POST'])
@jwt_required()
def create_skill():
    data = request.get_json()
    user_id = get_jwt_identity()
    skill_name = data.get('skill_name')
    description = data.get('description')
    category = data.get('category')

    new_skill = Skill(user_id=user_id, skill_name=skill_name, description=description, category=category)

    db.session.add(new_skill)
    db.session.commit()

    return jsonify({'message': 'Skill added successfully'}), 201

@skill_bp.route('/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify([{
        'id': skill.id,
        'user': User.query.get(skill.user_id).username,
        'skill_name': skill.skill_name,
        'description': skill.description,
        'category': skill.category
    } for skill in skills]), 200
from flask import render_template, redirect, url_for, flash, session, request
from models import db, Skill, User
from .forms import SkillForm

# View user's skills (GET)
def view_skills():
    if 'user_id' not in session:
        flash('You need to log in to view your skills', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_skills = Skill.query.filter_by(user_id=user_id).all()

    return render_template('skills.html', skills=user_skills)

# Add a new skill (GET, POST)
def add_skill():
    if 'user_id' not in session:
        flash('You need to log in to add a skill', 'danger')
        return redirect(url_for('auth.login'))

    form = SkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            name=form.name.data,
            description=form.description.data,
            user_id=session['user_id']
        )
        db.session.add(new_skill)
        db.session.commit()

        flash('Skill added successfully!', 'success')
        return redirect(url_for('skills.view_skills'))

    return render_template('add_skill.html', form=form)

# Edit an existing skill (GET, POST)
def edit_skill(skill_id):
    if 'user_id' not in session:
        flash('You need to log in to edit your skill', 'danger')
        return redirect(url_for('auth.login'))

    skill = Skill.query.get_or_404(skill_id)

    # Ensure the logged-in user owns the skill
    if skill.user_id != session['user_id']:
        flash('You are not authorized to edit this skill', 'danger')
        return redirect(url_for('skills.view_skills'))

    form = SkillForm(obj=skill)

    if form.validate_on_submit():
        skill.name = form.name.data
        skill.description = form.description.data
        db.session.commit()

        flash('Skill updated successfully!', 'success')
        return redirect(url_for('skills.view_skills'))

    return render_template('edit_skill.html', form=form)
cat: static/css: Is a directory
cat: static/js: Is a directory
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login to SkillSwap</h2>
    <form action="/login" method="POST">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="/signup">Sign up here</a></p>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Messages</title>
</head>
<body>
    <h2>Your Messages</h2>
    <ul>
        {% for message in messages %}
        <li>From: {{ message.sender }} - To: {{ message.recipient }} <br> {{ message.content }} <br> Sent on: {{ message.timestamp }}</li>
        {% endfor %}
    </ul>

    <h3>Send a Message</h3>
    <form action="/messages" method="POST">
        <label for="recipient_id">Recipient ID:</label>
        <input type="text" id="recipient_id" name="recipient_id" required><br><br>

        <label for="content">Message:</label>
        <textarea id="content" name="content" required></textarea><br><br>

        <input type="submit" value="Send Message">
    </form>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposals</title>
</head>
<body>
    <h2>Your Proposals</h2>
    <ul>
        {% for proposal in proposals %}
        <li>Offering {{ proposal.offer_skill_id }} for {{ proposal.request_skill_id }} - Status: {{ proposal.status }}</li>
        {% endfor %}
    </ul>

    <h3>Create a New Proposal</h3>
    <form action="/proposals" method="POST">
        <label for="offer_skill_id">Offer Skill ID:</label>
        <input type="text" id="offer_skill_id" name="offer_skill_id" required><br><br>

        <label for="request_skill_id">Request Skill ID:</label>
        <input type="text" id="request_skill_id" name="request_skill_id" required><br><br>

        <input type="submit" value="Create Proposal">
    </form>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ratings</title>
</head>
<body>
    <h2>Rate a User</h2>
    <form action="/ratings" method="POST">
        <label for="user_id">User ID:</label>
        <input type="text" id="user_id" name="user_id" required><br><br>

        <label for="partner_id">Partner ID:</label>
        <input type="text" id="partner_id" name="partner_id" required><br><br>

        <label for="rating">Rating (out of 5):</label>
        <input type="number" id="rating" name="rating" min="1" max="5" required><br><br>

        <label for="review">Review:</label>
        <textarea id="review" name="review"></textarea><br><br>

        <input type="submit" value="Submit Rating">
    </form>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
</head>
<body>
    <h2>Sign Up for SkillSwap</h2>
    <form action="/signup" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Sign Up">
    </form>
    <p>Already have an account? <a href="/login">Login here</a></p>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skills</title>
</head>
<body>
    <h2>Available Skills</h2>
    <ul>
        {% for skill in skills %}
        <li>{{ skill.skill_name }} ({{ skill.category }}) - by {{ skill.user }}</li>
        {% endfor %}
    </ul>

    <h3>Add a New Skill</h3>
    <form action="/skills" method="POST">
        <label for="skill_name">Skill Name:</label>
        <input type="text" id="skill_name" name="skill_name" required><br><br>

        <label for="description">Description:</label>
        <textarea id="description" name="description" required></textarea><br><br>

        <label for="category">Category:</label>
        <input type="text" id="category" name="category" required><br><br>

        <input type="submit" value="Add Skill">
    </form>
</body>
</html>
