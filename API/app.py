# -*- coding: utf-8 -*-
# la structure minimale d’un serveur Flask
from flask import Flask

app = Flask(__name__)

# typique Flask: un décorateur (commence par @) et situé au-dessus d’une définition de fonction.
# @ sont utilisés pour associer une URL à une fonction. Ici, on associe la fonction  "hello"  à l’URL "/".
@app.route("/")
def hello():
    return "Hello World!"

# app.run() lance le serveur, et nous lui demandons par  "debug=True"  d’afficher l’aide au débogage en cas d’erreur dans le code.
# penser à désactiver cette option si vous souhaitez mettre votre site en ligne.
if __name__ == "__main__":
    app.run(debug=True)