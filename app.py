import csv

import SpellChecker as SpellChecker
from flask import Flask,request,jsonify
import os
import re
#from flask_cors import CORS,cross_origin

# Create the flask app
app = Flask(__name__)

# Recupérer le chemin ou repertoire courant
path = os.getcwd()

# Création du repertoire qui doit contenir les images uploadés et les images obtenues après application de l'OCR
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

# Dossier contenant les fichiers CSV
CSV_FOLDER  = os.path.join(path,'csv')

# Configuration de ces repertoires
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

app.config['MAX_CONTENT_LENGHT'] = 10*1024*1024



# Liste des extensions autorisees pour upload des fichiers
ALLOWED_EXTENSIONS  = set(['txt','pdf','png','jpg','jpeg','gif'])



# routes

# Fonction de test  qui retourne le carré (rien à avoir avec notre projet d'OCR)
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




###############################################################################################################################
#####################     DIFFERENTES FONCTIONS CONCERNANT LE PRÉTRAITEMENT ET L'APPLICATION DU PROCÉDÉ D'OCR   ##############
###############################################################################################################################


# Fonction pour génerer des fichiers CSV à partir du resultat de l'opération de Pytesseract sur les images de bilan sanguins
# au format ".txt"
# Cette fonction prend comme paramètre :
# => entrée : fichier txt du resultat de l'OCR avec Pytesseract
def write_csv_file(output_file,i):
    header = ['Element', 'Unite', 'Valeur_obtenu', 'Valeur_reference', 'Anteriorite']
    if not os.path.isdir(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)

    csv_file = CSV_FOLDER + '/'+'bilan_result_%s.csv'%str(i)

    print("csv file :",csv_file)
    print("output file :",output_file)

    with open(csv_file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        fichier2 = open("correction0.txt", "a")
        spell = SpellChecker(language=None, distance=1)
        spell.word_frequency.load_dictionary('medicaleJson.json')
        with open('datasetDcp.txt') as f:
            dictionnary = ['' + line.rstrip() for line in f]
        file = open(output_file, "r")

        fichier = open("dataResult0.txt", "a")
        with open('uniteBilan.txt') as f:
            uniteBilan = ['' + uniteB.rstrip() for uniteB in f]
        for line in file:
            correct_output = []
            output = '' + line.rstrip()
            listOutput = output.split()
            misspelled = spell.unknown(listOutput)
            for word in listOutput:
                correct_output.append(spell.correction(word))
            output = ' '.join(correct_output)
            fichier2.write(output + "\n")
            for element in dictionnary:
                correct_ligne = output if element.lower() in output.lower() else None
                if correct_ligne is None:
                    pass
                else:
                    correct_ligne = re.sub('([^\\w^*^<^>^=]{3,}[A-Za-z]*)(\\s*[a-zA-Z])*', ' ', correct_ligne)
                    if re.search('([^\\d]+\\d+){2,}', correct_ligne):
                        for unite in uniteBilan:
                            # print(correct_ligne)
                            # unite = ''+unit.rstrip()
                            # print(unite)
                            valeur = re.search(
                                '\\W+\\d+\\W?\\d*\\s' + unite + '\\s\\d+\\W?\\d*\\s\\w?\\s\\d+\\W?\\d*(\\s\\d+\\W?\\d*)?',
                                correct_ligne)
                            # print(valeur)
                            if valeur:
                                valeurBilan = valeur.group(0)
                                # print("mdr")
                                print(" {} {} ".format(element, valeurBilan))
                                print("")
                                data = []
                                data.append(element)
                                data.append(unite)
                                valeurBilan = re.sub(unite, '####', valeurBilan)
                                valeur_obtenu = re.search(r'\d+\W?\s?\d+\s?####', valeurBilan)
                                valeurBilan = re.sub(r'\d+\W?\s?\d+\s?####', '', valeurBilan)
                                if valeur_obtenu:
                                    data.append(valeur_obtenu.group(0).rstrip('####'))

                                valeur_reference = re.search(r'\d+\W\d+\s?à\s?\d+\W\d+', valeurBilan)

                                if valeur_reference:
                                    data.append(valeur_reference.group(0))
                                valeurBilan = re.sub(r'\d+\W\d+\s?à\s?\d+\W\d+', '', valeurBilan)

                                anteriorite = re.search(r'\d+\W?\s?\d+\W?\d*', valeurBilan)

                                if anteriorite:
                                    data.append(anteriorite.group(0))

                                writer.writerow(data)
                                # fichier.write("\n\n"+correct_ligne+"\n\n")
                                break
                            else:
                                pass
                    else:
                        pass
    fichier.close()
    fichier2.close()






if __name__=='__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True,threaded=True,port=5000)