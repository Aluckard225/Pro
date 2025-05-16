from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, User, Car, Feature, init_db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import MetaData


metadata = MetaData()
app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mashina.db'
app.config['SECRET_KEY'] = "123"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/api/cars')
def get_cars():
    try:
        cars = Car.query.order_by(Car.name).all()
        return jsonify([car.to_dict() for car in cars])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cars', methods=['POST'])
def add_car():
    data = request.get_json()
    
    try:
        car = Car(
            name=data['name'],
            year=data['year'],
            color=data['color'],
            mileage=data['mileage'],
            engine=data['engine'],
            power=data['power'],
            transmission=data['transmission'],
            drive=data['drive'],
            price=data['price']
        )
        db.session.add(car)
        db.session.commit()
        for category in ['comfort', 'safety', 'media']:
            for feature in data.get(category, []):
                feat = Feature(
                    car_id=car.id,
                    category=category,
                    feature=feature
                )
                db.session.add(feat)
        
        db.session.commit()
        return jsonify({'success': True, 'car': car.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.get_json()
    
    try:
        car.name = data.get('name', car.name)
        car.year = data.get('year', car.year)
        car.color = data.get('color', car.color)
        car.mileage = data.get('mileage', car.mileage)
        car.engine = data.get('engine', car.engine)
        car.power = data.get('power', car.power)
        car.transmission = data.get('transmission', car.transmission)
        car.drive = data.get('drive', car.drive)
        car.price = data.get('price', car.price)
        Feature.query.filter_by(car_id=car.id).delete()
        for category in ['comfort', 'safety', 'media']:
            for feature in data.get(category, []):
                feat = Feature(
                    car_id=car.id,
                    category=category,
                    feature=feature
                )
                db.session.add(feat)
        
        db.session.commit()
        return jsonify({'success': True, 'car': car.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    try:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
            if User.query.filter_by(username=username).first():
                return redirect(url_for('register', error='user_porno'))
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)  
            
            return jsonify({'success': True, 'redirect': url_for('index')})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Неверное имя пользователя или пароль'}), 401
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('index')})
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        init_db(app)
    app.run(debug=True)