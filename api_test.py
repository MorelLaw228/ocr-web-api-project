import requests

# Il s'agit d'un code pour tester de manière locale l'API developpé prcédemment avec Flask
#  (contenue dans le fichier source "app.py")
post_data = [{
                "0":5,
                "1":8,
                "2":15
            }]

#url = 'https://square-flask-api.herokuapp.com/square/'
url = 'https://ocr-web-api-project.herokuapp.com/square/'
#url = ' http://127.0.0.1:5000/square/'

response = requests.post(url, json=post_data)
print(response.text)