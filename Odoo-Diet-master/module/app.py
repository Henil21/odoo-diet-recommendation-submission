from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from module import db,User
import google.generativeai as genai
from module import app


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # In-memory user storage (for demonstration purposes)
# users = {}


# @login_manager.user_loader
# def load_user(user_id):
#     if user_id in users:
#         return User(user_id)
#     return None

# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         return render_template('index.html', name=users[current_user.id]['name'])
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         # Redirect authenticated users to the homepage
#         return redirect(url_for('index'))

#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
        
#         # Assuming users is a dictionary with email as key and user info as value
#         # This should be replaced with a database query in a production application
#         user = User.query.filter_by(email=email).first()
        
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid email or password')

#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         name = request.form['name']
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email address already exists')
#         else:
#             new_user = User(email=email, password=generate_password_hash(password), name=name)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account created successfully. Please log in.')
#             return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
@app.route('/api/calculate', methods=['POST'])
@login_required
def calculate():
    data = request.json
    age = data['age']
    gender = data['gender']
    height = data['height']
    weight = data['weight']
    activity_level = data['activity_level']
    dietary_preferences = data['dietary_preferences']
    allergies = data['allergies']
    goal = data['goal']

    GOOGLE_API_KEY = 'AIzaSyBOye96WGVStgXX2Tc0iw2HlAAfrkDDVAI'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    prompt = f"Give me a diet plan recommendation for the following data: age {age}, gender {gender}, height {height} cm, weight {weight} kg, activity level {activity_level}, dietary preferences {dietary_preferences}, allergies {allergies}, goal {goal}."
    response = model.generate_content([prompt])
    
    # Assuming response contains the generated diet plan in response['text']
    diet_plan = response['text']
    
    return jsonify({'data': diet_plan})

if __name__ == '__main__':
    app.run(debug=True)

