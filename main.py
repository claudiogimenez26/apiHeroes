from flask import Flask,request,jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import db, Heroes

db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/heroes"
try:
    # Intenta crear una conexión al motor de la base de datos
    engine = create_engine(db_url)
    connection = engine.connect()

    # Si no se produce ninguna excepción, la conexión fue exitosa
    print("Conexión exitosa a la base de datos")

    # Puedes realizar más operaciones con la base de datos aquí

    # Cierra la conexión
    connection.close()

except SQLAlchemyError as e:
    # Si ocurre algún error al conectar, muestra un mensaje de error
    print(f"Error al conectar a la base de datos: {e}")

app = Flask(__name__)
port = 5000
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route("/")
def hello_world():
    return 'Hello World!'

@app.route("/heroes", methods=['GET'])
def get_heroes():
    try:
        heroes = Heroes.query.all()
        heroes_data = []
        for heroe in heroes:
            heroe_data = {
                'id': heroe.id,
                'name': heroe.name,
                'alignment': heroe.alignment,
                'publisher': heroe.publisher,
                'names': heroe.names,
                'race': heroe.race,
                'gender': heroe.gender,
                'image': heroe.image
            }
            heroes_data.append(heroe_data)
        return jsonify({'heroes': heroes_data})    
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server errores'}), 500

@app.route("/heroes",methods=['POST'])
def add_heroes():
    try:
        data= request.json
        name= data.get('name')
        if not name :
            return jsonify({'message': 'Bad request, name not found'}), 400
        alignment= data.get('alignment')
        if not alignment :
            return jsonify({'message': 'Bad request, alignment not found'}), 400
        publisher= data.get('publisher')
        if not publisher :
            return jsonify({'message': 'Bad request, publisher not found'}), 400
        names= data.get('names')
        if not names :
            return jsonify({'message': 'Bad request, names not found'}), 400
        race= data.get('race')
        if not race :
            return jsonify({'message': 'Bad request, race not found'}), 400
        gender= data.get('gender')
        if not gender :
            return jsonify({'message': 'Bad request, gender not found'}), 400
        image= data.get('image')
        if not image :
            return jsonify({'message': 'Bad request, image not found'}), 400
        new_heroe = Heroes(name=name, alignment=alignment, publisher=publisher, names=names,race=race, gender=gender, image=image)
        db.session.add(new_heroe)
        db.session.commit()
        return jsonify({'heroe':{'id':new_heroe.id,'name':new_heroe.name,'alignment':new_heroe.alignment, 'publisher':new_heroe.publisher,'names':new_heroe.names,'race':new_heroe.race,'gender':new_heroe.gender,'image':new_heroe.image}}),201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', debug=True, port=port)