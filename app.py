from flask import Flask,request,jsonify


# Create the flask app
app = Flask(__name__)


# routes

# Fonction de test  qui retourne le carré (reien à avoir avec notre projet d'OCR)
@app.route('/square/', methods=['POST'])
def square():
    # get data
    data = request.get_json()[0]
    num_list = data.values()

    response = {}
    response['results'] = []

    for n in num_list:
        square = n ** 2
        response['results'].append(square)

    return jsonify(response)

# Fonction qui permet d'envoyer des requêtes HTTP  en GET (rien à  avoir avec notre projet d'OCR ) Test !!!!
@app.route('/getmsg/',methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Bienvenue  {name}  sur notre merveilleuse plateforme !!"

    # Return the response in json format
    return jsonify(response)

# Fonction qui permet d'envoyer des requêtes HTTP  en POST (rien à  avoir avec notre projet d'OCR ) Test !!!!
# Retourne la reponse de la requête au format JSON
@app.route('/post/',methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Bienvenue à toi  {param} sur notre merveilleuse plateforme !!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# Un message d'acceuil pour tester notre serveur
@app.route('/')
def mon_index():
    return "<h1> Bienvenue sur notre serveur .<h1>"

if __name__=='__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True,threaded=True,port=5000)