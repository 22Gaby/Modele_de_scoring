# création API pour Projet7- OCR
import json
import pandas as pd
import pickle
from flask import Flask, render_template, send_file, url_for


# lecture du df contenant les données test avec 173 features + best_modele_lgbm
df_test= pd.read_csv('./API/ressources/data_csv/df_test_features_173_500clients.csv')
id_clients = list(df_test['SK_ID_CURR'])
with open('./API/ressources/modele/model_best_lgbm.pickle', 'rb') as obj:
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
    :return: score client
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
    return send_file('./ressources/data_csv/df_info_pret_client_500clients.csv')


@app.route("/csv_df_test/")
def csv_df_test():
    '''
    Définition route pour acceder au dataframe avec données de test pour le modele
    :return: file_csv
    '''
    return send_file('./ressources/data_csv/df_test_features_173_500clients.csv')


if __name__ == "__main__":
    app.run(debug=True)