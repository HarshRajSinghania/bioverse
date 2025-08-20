from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from bioverse_app import BioVerseApp

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize BioVerse app
bioverse_app = BioVerseApp()

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    saved_aliens = db.relationship('SavedAlien', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Extreme Environment Model
class ExtremeEnvironment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # volcanic, frozen, oceanic, etc.
    temperature = db.Column(db.String(50))
    atmosphere = db.Column(db.String(200))
    gravity = db.Column(db.Float)
    description = db.Column(db.Text)
    challenges = db.Column(db.Text)

# Saved Alien Model
class SavedAlien(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_name = db.Column(db.String(100), nullable=False)
    planet_data = db.Column(db.JSON)
    alien_data = db.Column(db.JSON)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    environment_explorations = db.relationship('EnvironmentExploration', backref='saved_alien', lazy=True)

# Environment Exploration Model
class EnvironmentExploration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saved_alien_id = db.Column(db.Integer, db.ForeignKey('saved_alien.id'), nullable=False)
    environment_id = db.Column(db.Integer, db.ForeignKey('extreme_environment.id'), nullable=False)
    survival_analysis = db.Column(db.JSON)
    narrative_outcome = db.Column(db.Text)
    survival_score = db.Column(db.Integer)  # 0-100
    explored_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    environment = db.relationship('ExtremeEnvironment')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/create-alien', methods=['POST'])
@login_required
def create_alien():
    """Create alien species based on planet name"""
    try:
        data = request.get_json()
        print(f"Incoming request data: {data}")
        planet_name = data.get('planetName', '').strip()
        
        if not planet_name:
            return jsonify({'error': 'Planet name is required'}), 400
        
        # Analyze planet
        print(f"Analyzing planet: {planet_name}")
        planet_data = bioverse_app.analyze_planet(planet_name)
        print(f"Planet data received: {planet_data}")
        
        # Generate alien
        print(f"Generating alien for planet: {planet_data['name']}")
        alien_data = bioverse_app.generate_alien(planet_data)
        print(f"Alien data received: {alien_data}")
        
        # Stage 4: Generate optimized image prompt using AI
        print(f"Generating optimized image prompt for alien...")
        image_prompt = bioverse_app.generate_image_prompt(planet_data, alien_data)
        print(f"AI-generated image prompt: {image_prompt}")
        
        # Stage 5: Generate image using AI-optimized prompt
        print(f"Generating image with AI-optimized prompt...")
        image_url = bioverse_app.generate_image(image_prompt)
        print(f"Image URL received: {image_url}")
        
        # Return all data
        result = {
            'planet': planet_data,
            'alien': alien_data,
            'image': image_url
        }
        print(f"Returning result: {result}")
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in create_alien endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Flask server is running'})

@app.route('/api/save-alien', methods=['POST'])
@login_required
def save_alien():
    """Save generated alien to user's collection"""
    try:
        data = request.get_json()
        
        saved_alien = SavedAlien(
            user_id=current_user.id,
            planet_name=data['planet']['name'],
            planet_data=data['planet'],
            alien_data=data['alien'],
            image_url=data['image']
        )
        
        db.session.add(saved_alien)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'alien_id': saved_alien.id,
            'message': 'Alien saved successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved-aliens')
@login_required
def get_saved_aliens():
    """Get user's saved aliens"""
    try:
        aliens = SavedAlien.query.filter_by(user_id=current_user.id)\
            .order_by(SavedAlien.created_at.desc()).all()
        
        return jsonify([{
            'id': alien.id,
            'planet_name': alien.planet_name,
            'planet_data': alien.planet_data,
            'alien_data': alien.alien_data,
            'image_url': alien.image_url,
            'created_at': alien.created_at.isoformat()
        } for alien in aliens]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/environments')
def get_environments():
    """Get all extreme environments"""
    try:
        environments = ExtremeEnvironment.query.all()
        return jsonify([{
            'id': env.id,
            'name': env.name,
            'type': env.type,
            'temperature': env.temperature,
            'atmosphere': env.atmosphere,
            'gravity': env.gravity,
            'description': env.description,
            'challenges': env.challenges
        } for env in environments]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/explore-environment', methods=['POST'])
@login_required
def explore_environment():
    """Explore how an alien would survive in an extreme environment"""
    try:
        data = request.get_json()
        alien_id = data['alien_id']
        environment_id = data['environment_id']
        
        # Get alien and environment data
        alien = SavedAlien.query.get_or_404(alien_id)
        environment = ExtremeEnvironment.query.get_or_404(environment_id)
        
        # Generate survival analysis using AI
        survival_analysis = bioverse_app.analyze_survival(
            alien.alien_data,
            environment
        )
        
        # Create exploration record
        exploration = EnvironmentExploration(
            saved_alien_id=alien_id,
            environment_id=environment_id,
            survival_analysis=survival_analysis['analysis'],
            narrative_outcome=survival_analysis['narrative'],
            survival_score=survival_analysis['survival_score']
        )
        
        db.session.add(exploration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'exploration': {
                'id': exploration.id,
                'environment': {
                    'name': environment.name,
                    'type': environment.type,
                    'description': environment.description
                },
                'survival_analysis': exploration.survival_analysis,
                'narrative_outcome': exploration.narrative_outcome,
                'survival_score': exploration.survival_score,
                'explored_at': exploration.explored_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alien-explorations/<int:alien_id>')
@login_required
def get_alien_explorations(alien_id):
    """Get all environment explorations for a specific alien"""
    try:
        # Verify alien belongs to current user
        alien = SavedAlien.query.filter_by(
            id=alien_id,
            user_id=current_user.id
        ).first_or_404()
        
        explorations = EnvironmentExploration.query.filter_by(
            saved_alien_id=alien_id
        ).order_by(EnvironmentExploration.explored_at.desc()).all()
        
        return jsonify([{
            'id': exp.id,
            'environment': {
                'name': exp.environment.name,
                'type': exp.environment.type,
                'description': exp.environment.description
            },
            'survival_analysis': exp.survival_analysis,
            'narrative_outcome': exp.narrative_outcome,
            'survival_score': exp.survival_score,
            'explored_at': exp.explored_at.isoformat()
        } for exp in explorations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/saved-aliens')
@login_required
def saved_aliens():
    """Display user's saved aliens page"""
    return render_template('saved_aliens.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Here you would typically send an email or store in database
        # For now, we'll just return a success response
        print(f"Contact form submitted: {data}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We\'ll get back to you soon.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test-image', methods=['POST'])
@login_required
def test_image():
    """Test endpoint for debugging image generation"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'A simple alien creature')
        
        # Use a simple placeholder to avoid API issues
        placeholder_url = "https://via.placeholder.com/1024x1024/0a0a2e/00ffff?text=Alien+Creature"
        
        return jsonify({
            'success': True,
            'image': placeholder_url,
            'message': 'Using placeholder image - API keys may need configuration'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def init_environments():
    """Initialize extreme environments in database"""
    environments = [
        {
            'name': 'Volcanic Inferno',
            'type': 'volcanic',
            'temperature': '800-1200°C',
            'atmosphere': 'Sulfur dioxide, carbon monoxide, volcanic ash',
            'gravity': 2.5,
            'description': 'A world of molten rock and constant eruptions where rivers of lava carve the landscape',
            'challenges': 'Extreme heat, toxic atmosphere, seismic activity, molten surfaces'
        },
        {
            'name': 'Frozen Wasteland',
            'type': 'frozen',
            'temperature': '-200 to -150°C',
            'atmosphere': 'Thin nitrogen-methane mix, ice crystals',
            'gravity': 0.8,
            'description': 'A dark frozen world where even gases freeze solid and ice mountains reach the sky',
            'challenges': 'Extreme cold, brittle structures, limited energy sources, frozen atmosphere'
        },
        {
            'name': 'Deep Ocean Abyss',
            'type': 'oceanic',
            'temperature': '2-4°C',
            'atmosphere': 'High-pressure water, dissolved minerals',
            'gravity': 1.2,
            'description': 'An endless ocean world with crushing pressures and bioluminescent life in eternal darkness',
            'challenges': 'Crushing pressure, no light, limited oxygen, corrosive water'
        },
        {
            'name': 'Radiation Storm',
            'type': 'irradiated',
            'temperature': '-50 to 50°C',
            'atmosphere': 'Ionized particles, radioactive isotopes',
            'gravity': 1.0,
            'description': 'A planet bathed in constant radiation storms with glowing auroras and charged particles',
            'challenges': 'Lethal radiation, electromagnetic interference, genetic damage, ionizing atmosphere'
        },
        {
            'name': 'Crystal Desert',
            'type': 'crystalline',
            'temperature': '-100 to 200°C',
            'atmosphere': 'Silicate particles, crystal dust',
            'gravity': 1.8,
            'description': 'A world of sharp crystal formations where silicon-based life might emerge',
            'challenges': 'Abrasive crystals, temperature extremes, sharp terrain, limited organic compounds'
        }
    ]
    
    for env_data in environments:
        if not ExtremeEnvironment.query.filter_by(name=env_data['name']).first():
            env = ExtremeEnvironment(**env_data)
            db.session.add(env)
    
    db.session.commit()

# Create database tables and initialize environments
with app.app_context():
    db.create_all()
    init_environments()

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)