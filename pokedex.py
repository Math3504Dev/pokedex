from flask import Flask, request, jsonify, send_from_directory
import csv

app = Flask(__name__, static_folder='.', static_url_path='')

# Charger les données une seule fois au démarrage
def load_data():
    pokemon_data = []
    images_data = {}

    # Charger les données Pokémon
    with open('pokedex_francais_complet.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokemon_data.append(row)

    # Charger les images
    with open('pokemon_images.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            images_data[row['Numéro']] = row

    # Fusionner les données
    for pokemon in pokemon_data:
        numero = pokemon['Numéro']
        if numero in images_data:
            pokemon.update(images_data[numero])

    return pokemon_data

df = load_data()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        results = df
    else:
        results = [
            pokemon for pokemon in df if (
                query in pokemon['Nom'].lower() or
                query in pokemon['Type 1'].lower() or
                query in pokemon['Type 2'].lower() or
                query in str(pokemon['Numéro'])
            )
        ]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)