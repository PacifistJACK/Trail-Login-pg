from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import db, init_app

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a more secure key
init_app(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('signup'))

        if '@' not in email or '.' not in email:
            flash('Invalid email format. Please enter a valid email address.', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Sign-Up successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Email or Username already exists.', 'danger')
    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your Dashboard!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures database tables are created
    app.run(debug=True)
