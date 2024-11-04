from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Utworzenie aplikacji Flask
app = Flask(__name__)

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)

# Definicja modelu
class User(db.Model):
    __tablename__ = 'users'  # Nazwa tabeli w bazie danych

    id = db.Column(db.Integer, primary_key=True)  # Kolumna id (klucz główny)
    name = db.Column(db.String(80), nullable=False)  # Kolumna name (niepusta)
    surname = db.Column(db.String(80), nullable=False)  # Kolumna surname (niepusta)
    position = db.Column(db.String(80), nullable=False)  # Kolumna position (niepusta)
    age = db.Column(db.Integer)  # Kolumna age (opcjonalna)
    height = db.Column(db.Float)  # Kolumna height (opcjonalna)

    def __repr__(self):
        return f'<User {self.name} {self.surname}>'

# Tworzenie tabeli
with app.app_context():
    # db.drop_all() 
    db.create_all()  # Tworzy tabele na podstawie zdefiniowanych modeli

# Definiowanie trasy
@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Dodawanie nowego użytkownika
        data = request.json
        new_user = User(
            name=data['name'],
            surname=data['surname'],
            position=data['position'],
            age=data.get('age'),
            height=data.get('height')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

    elif request.method == 'GET':
        # Pobieranie listy użytkowników
        users = User.query.all()
        return jsonify([{"id": user.id, "name": user.name, "surname": user.surname,
                         "position": user.position, "age": user.age, "height": user.height} for user in users]), 200

# Uruchamianie aplikacji
if __name__ == "__main__":
    app.run(debug=True)


# CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     surname TEXT NOT NULL,
#     position TEXT NOT NULL,
#     age INTEGER,
#     hight REAL
# );
