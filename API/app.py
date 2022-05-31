# création API pour Projet7- OCR
import json
import pandas as pd
import pickle
from flask import Flask, render_template, send_file, url_for
from pathlib import Path


origin_path=Path('./')
ressources_path = origin_path.joinpath('ressources')
modele_path = ressources_path.joinpath('modele')
data_csv_path = ressources_path.joinpath('data_csv')

ressources1_path = data_csv_path.joinpath('df_test_features_173_500clients.csv')
modele1_path = modele_path.joinpath('model_best_lgbm.pickle')
ressources2_path = data_csv_path.joinpath('df_info_pret_client_500clients.csv')


df_test= pd.read_csv(ressources1_path)


id_clients = list(df_test['SK_ID_CURR'])
with open(modele1_path, 'rb') as obj:
    modele_best = pickle.load(obj)
    print(modele_best)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Bienvenu sur mon Projet 7"

@app.route('/calculate_score/<id_client>')
def calculate_score(id_client:int):
    '''
    Calcule le score du client à partir de son id avec best modele_lgbm
    :param id_client:
    :return: score client, score_classe
    '''
    df_id_client = df_test[df_test['SK_ID_CURR'] == int(id_client)]
    X_test_id_client = df_id_client.drop('SK_ID_CURR', axis=1)
    y_proba_id_client = modele_best.predict_proba(X_test_id_client)[:, 1]
    score_id_client = int(round(y_proba_id_client[0] * 100, 2))
    score_classe = modele_best.predict(X_test_id_client)[0]
    dic = {"score_client": float(score_id_client), "score_classe": str(score_classe)}
    # encodage du dic en objet json
    dic = json.dumps(dic)
    return dic





@app.route("/csv_info_pret_client/")
def csv_info_pret_client():
    '''
    Définition route pour acceder aux infos clients
    :return: file_csv
    '''
    return send_file(ressources2_path)


@app.route("/csv_df_test/")
def csv_df_test():
    '''
    Définition route pour acceder au dataframe avec données de test pour le modele
    :return: file_csv
    '''
    return send_file(ressources1_path)


if __name__ == "__main__":
    app.run(debug=True)