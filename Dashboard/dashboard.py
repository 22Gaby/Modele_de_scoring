from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests
import plotly.express as px
import pandas as pd
import json
from pathlib import Path

# version ID_CLIENT statique (selection du ID du premier client)
ID_CLIENT = 320753
origin_path=Path('./')
temp_path = origin_path.joinpath('temp')
csv_info_pret_client_path = temp_path.joinpath('df_info_pret_client_500clients.csv')
csv_test_df_path = temp_path.joinpath('df_test_features_173_500clients.csv')
csv_features_imp_df_path = temp_path.joinpath('df_features_imp_dashboard.csv')


r_csv_info_pret = requests.get('http://127.0.0.1:5000/csv_info_pret_client/')
open(csv_info_pret_client_path, "wb").write(r_csv_info_pret.content)
csv_info_pret_client = pd.read_csv(csv_info_pret_client_path)

r_features_imp = requests.get('http://127.0.0.1:5000/csv_df_features_imp/')
open(csv_features_imp_df_path, "wb").write(r_features_imp.content)
csv_features_imp_df = pd.read_csv(csv_features_imp_df_path)

r_test = requests.get('http://127.0.0.1:5000/csv_df_test/')
open(csv_test_df_path, "wb").write(r_test.content)
csv_test_df = pd.read_csv(csv_test_df_path)

chart2 = px.scatter(data_frame=csv_features_imp_df,
                    x=csv_features_imp_df.columns[7],
                    y=csv_features_imp_df.columns[9],
                    color=csv_features_imp_df['SCORE_CLIENT'],
                    title=f"Graphique analyse {csv_features_imp_df.columns[9]} vs {csv_features_imp_df.columns[7]}",
                    )

chart3 = px.histogram(data_frame=csv_features_imp_df,
                      x=csv_features_imp_df.columns[11],
                      histnorm='percent',
                      color=csv_features_imp_df['PRED_CLASSE'],
                      barmode='overlay',
                      title=f"Distribution de {csv_features_imp_df.columns[11]} selon les classes",
                      )



# figure de jauge sous plotly
fig_jauge = go.Figure()

ind= go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    # next value = score_client par rapport une proba_seuil de 47
    value = 30,
    mode = "gauge+number+delta",
    delta = {'reference': 57,
             'increasing': {'color': 'Crimson'},
             'decreasing': {'color': 'Green'}},
    gauge = {'axis': {'range': [None, 100],
                      'tickwidth': 3,
                      'tickcolor': 'darkblue'},
             'bar': {'color': 'white', 'thickness' : 0.10},
             'steps': [{'range': [0, 25], 'color': 'Green'},
                       {'range': [25, 49.49], 'color': 'LimeGreen'},
                       {'range': [49.5, 50.5], 'color': 'red'},
                       {'range': [50.51, 75], 'color': 'Orange'},
                       {'range': [75, 100], 'color': 'Crimson'}],
             'threshold': {'line': {'color': 'white', 'width': 10},
                            'thickness': 0.35, 'value': 57}})
fig_jauge.add_trace(ind)

fig_jauge.update_layout(paper_bgcolor='white',
                        height=250, width=300,
                        font={'color': 'darkblue', 'family': 'Arial'},
                        margin=dict(l=0, r=0, b=0, t=0, pad=0))



app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])


dropdown1_scatter_test_df = dcc.Dropdown(
        id="dropdown1_scatter_test_df",
        options=[{"value":feature, "label":feature} for feature in csv_features_imp_df.drop(['Sexe', 'Niveau éducation', 'Statut familial'], axis=1).columns[4:]],
        value=csv_features_imp_df.columns[7],
        clearable = False )


dropdown2_scatter_test_df = dcc.Dropdown(
        id="dropdown2_scatter_test_df",
        options=[{"value":feature, "label":feature} for feature in csv_features_imp_df.drop(['Sexe', 'Niveau éducation', 'Statut familial'], axis=1).columns[5:]],
        value=csv_features_imp_df.columns[9],
        clearable = False )

dropdown_bar_chart3 = dcc.Dropdown(
        id="dropdown_bar_chart3",
        options=[{"value":label, "label":label} for label in csv_features_imp_df.drop(['Sexe', 'Niveau éducation', 'Statut familial'], axis=1).columns[4:]],
        value=csv_features_imp_df.columns[11],
        clearable = False )


graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,)

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,)



row0 = html.Div(children=[
    html.Img(src=app.get_asset_url('python_logo_icon.png'), style={"height": "40px", "margin-left": "20px", }),
    html.Img(src=app.get_asset_url('Plotly-logo.png'), style={"height": "40px", "margin-left": "30px", }),
    html.Img(src=app.get_asset_url('scikit-learn-logo.png'), style={"height": "40px", "margin-left": "20px", }),
    html.Img(src=app.get_asset_url('pandas_logo.png'), style={"height": "40px", "margin-left": "30px", }),
])

header = html.H3(children="Welcome to 👨 Gabriela's Dashboard ")


# creation cards for row1: card_logo_row1 pour menu de gauche
card_logo_row1 = dbc.Card(
    dbc.CardImg(src=app.get_asset_url('logo.png'), top=False, bottom=True,
                title="Logo entreprise Prêt à dépenser",
                alt='Learn Dash Bootstrap Card Component'),)

# creation cards for row1: card_main_row1 pour menu de gauche
card_main_row1 = dbc.Card(
    [
        html.Div(children=[
            html.H1("🏠 Projet 7: Implémentez un modèle de scoring"),
            html.Br(),
            dcc.Markdown(
                '''L’entreprise intitulé **"Prêt à dépenser"**, souhaite mettre en œuvre un **outil de “scoring crédit”** pour calculer la probabilité qu’un client rembourse son crédit, 
                puis classifie la demande en crédit accordé ou refusé. 
                L’entreprise souhaite développer un **algorithme de classification** en s’appuyant sur des sources de données variées 
                (données comportementales, données provenant d'autres institutions financières, etc.)
               Prêt à dépenser décide de développer un **dashboard interactif**  
               facilement exploitable par les chargés de relation client afin d’expliquer les décisions d’octroi de crédit, 
               et de disposer des informations clients à explorer facilement.''',
                style={'white-space': 'pre', 'fontSize': 22}, ),
        ], ),
    ],
    color="#cee1eb", outline=True,
    style = {"margin-left": 0, "margin-right": 0,}
)

# creation cards for row2: card_main_row2 pour menu de gauche
card_main_row2 = dbc.Card(
    [
         dbc.CardBody([
             html.H3("API de prédiction solvabilité",  className="card-subtitle"),
             html.Br(),
             html.Br(),
                html.H4("🔎 Tapez ID Client pour modélisation prédiction",  className="card-subtitle"),
                html.Br(),
                dcc.Dropdown(csv_test_df.SK_ID_CURR, id='id_client_input',  placeholder="Select ID Client pour PREDICTION",
                 ),
                html.Br(),
                html.Br(),
                html.H4("📉 Jauge du Score de prédiction", className="card-subtitle", style={"background-color": "pink",}),
                html.Br(),
                dcc.Graph(figure=fig_jauge, id="my_jauge", )],
             style={"border-style": "groove","margin-left":"auto", "margin-right":"auto",
                    } ),
    ],
    color="#cee1eb",   # https://bootswatch.com/default/ for more card colors
    style = {"margin-left": 0, "margin-right": 0,}
    )

# creation cards for row2: card_question_row2 pour menu de droite
card_question_row2 = dbc.Card([
    dbc.CardBody([
        html.H3('👁️ Client Principal: Informations descriptives et demande de prêt :',
                ),
        html.Br(),
        html.H4('Données personnelles du Client :', ),
        dash_table.DataTable(csv_info_pret_client.to_dict('records'),
                             [{"name": i, "id": i} for i in csv_info_pret_client.columns[1:9]],
                             style_header={'backgroundColor': '#cee1eb', "font-family": "Times New Roman",'fontSize': 20, },
                            style_cell={'textAlign': 'center'},
                            style_data={'backgroundColor': '#cee1eb', "font-family": "Times New Roman", 'fontSize': 18,},
                            id='table1_info_client',
                                     ),
        html.Br(),
        html.H4('Données de la demande du crédit :', ),
        dash_table.DataTable(csv_info_pret_client.to_dict('records'),
                             [{"name": i, "id": i} for i in csv_info_pret_client.columns[9:14]],
                             style_header={'backgroundColor': '#cee1eb', "font-family": "Times New Roman", 'fontSize': 20,},
                            style_cell={'textAlign': 'center'},
                            style_data={'backgroundColor': '#cee1eb', "font-family": "Times New Roman", 'fontSize': 18, },
                             id='table2_info_client',
                                     ),
        html.Br(),
        html.H3('📉 Résultat de Prediction de la Solvabilité du Client Principal:',
                ),
        dcc.Markdown(
                "La prédiction de la probabilité que le Client rembourse le crédit est calculé "
                "via une API spécifique avec LGBMClassifier, le meilleur modèle optimisé."
                "Pour le Client  {id_client} la probabilité calculée via l’API est :  **{score_client}** \n "
                "L’algorithme de classification indique une solvabilité du client de **{score_classe}** \n "
                "Le prêt est accordé au Client : **{score_text}**",
                style={'white-space': 'pre', 'fontSize': 20, "font-family": "Times New Roman", },
                id='id_client_output_2',),
        ]),
    ], color="#cee1eb", )


# création row3:
header_row3 = html.H3(children="Visualisation des caractéristiques importantes pour la décision d’octroi de crédit ",
                      style={"background-color": "pink", "margin-left": 200, "margin-right": 200, "text-align": "center", })

text_buton = html.H5(children="Tapez ID pour visualisation position du Client Principal vis-à-vis des autres clients: ",
                      style={ "margin-left": 300, "margin-right": 500, "text-align": "center", })

button_input =html.Div(children=[
    dcc.Dropdown(csv_features_imp_df.SK_ID_CURR,
        placeholder='Entrer ID client pour visualisation',
        id='input_box_features',
        style={'textAlign': 'center', "margin-left": 200, "margin-right": 500,},
    )])

text_graphiques = html.H4(children="Graphiques de positionnement du Client Principal vis-à-vis des autres clients sur les caractéristiques importantes: ",
                      style={ "margin-left": 300, "margin-right": 500, "text-align": "center", })

scatter_div= html.Div(children=[
    dropdown1_scatter_test_df, dropdown2_scatter_test_df, html.Br(),graph2 ],
    style={'display': 'inline-block', "width": "40%", "background-color": "#cee1eb",})

bar_div = html.Div(children=[dropdown_bar_chart3, html.Br(),graph3],
                   style={'display': 'inline-block',"width": "40%",
                          "margin-left": "70px", "background-color": "#cee1eb",} )

row3= html.Div(children=[header_row3, html.Br(),  text_buton, button_input, html.Br(), html.Br(), text_graphiques, html.Br(), scatter_div, bar_div, html.Br(), ],)




# definition layout
layout = html.Div(children=[
    row0, header, html.Hr(),
    dbc.Row([dbc.Col(card_logo_row1, width={'size': 2, 'offset': 1}, ),
             dbc.Col(card_main_row1, width={'size': 9, 'offset': 0}),],),
    html.Hr(),


    html.H3(children="Les CLIENTS de la société - Prêt à dépenser -",
                      style={"background-color": "pink", "margin-left": 200, "margin-right": 200,
                             "text-align": "center"}),
    html.Br(),
    html.H4('Sélectionner l’identifiant ID du Client Principal:', style={ "font-family": "Times New Roman",
                                                      "margin-left":10,
                                                      }),
    dcc.Dropdown(csv_info_pret_client.SK_ID_CURR, id='id_client_info_input',
                 placeholder="320753", style={"width": "60%",
                                                               "margin-left":400,
                                                               }),
    html.Br(),
    html.Br(),

    dbc.Row([dbc.Col(card_main_row2, width={'size': 2, 'offset': 1, },),
             dbc.Col(card_question_row2, width=8),], justify="around"),
    html.Hr(),
    row3, html.Br(), html.Hr(),
], style={"text-align": "center","background-color": "#cee1eb",
          "font-family": "Times New Roman",})

app.layout = layout


# callback: Idclient --figure jauge -- score client
@app.callback(
    Output('my_jauge', 'figure'),
    Input('id_client_input', 'value'))
def update_gauge(id_client):
    if id_client is None:
        id_client = ID_CLIENT
    content_score_client = json.loads(requests.get(f'http://127.0.0.1:5000/calculate_score/{id_client}').content)
    score_client = content_score_client["score_client"]
    ind.value= score_client
    fig_jauge = go.Figure()
    fig_jauge.add_trace(ind)
    fig_jauge.update_layout(paper_bgcolor='white',
                            height=200, width=300,
                            font={'color': 'darkblue', 'family': 'Arial'},
                            margin=dict(l=20, r=30, b=0, t=0, pad=0))
    return fig_jauge


# callback: retour de prediction API score client en affichage text et score
@app.callback(
    Output(component_id='id_client_output_2', component_property='children'),
    Input(component_id='id_client_input', component_property='value'))
def search_info_client_dropdown(id_client):
    if id_client is None:
        return ""
    content_score_client = json.loads(requests.get(f'http://127.0.0.1:5000/calculate_score/{id_client}').content)
    score_client = content_score_client["score_client"]
    score_classe = content_score_client["score_classe"]
    if score_classe == "0":
        score_text = "OUI"
    else:
        score_text = "NON"
    return f'''
            La prédiction de la probabilité que le Client Principal rembourse le crédit est calculé via une API spécifique.
            Le meilleur modéle choisi est LGBMClassifier, avec les hyperparamètres optimisés. 
            Pour le Client  {id_client} la probabilité calculé via l’API est de :  **{score_client}%**
            Plus la probabilité est faible, plus le client est solvable. Le seuil maximum de solvabilité est de 57%.
            L’algorithme de classification indique le positionnement du client dans la classe **{score_classe}**
            La demande de crédit est accordée au Client Principal: **{score_text}**'''


# callback: bouton id_client - 2 tables: 1 ligne avec info client et 1 ligne avec prêt
@app.callback(
    [Output('table1_info_client', 'data'),
    Output('table2_info_client', 'data')],
    Input('id_client_info_input', 'value'))
def update_info_client(id_client):
    if id_client is None:
        id_client = ID_CLIENT
    csv_info_pret_client = pd.read_csv(csv_info_pret_client_path)
    csv_info_pret_client = csv_info_pret_client.set_index("SK_ID_CURR")
    csv_info_pret_client09 = csv_info_pret_client[csv_info_pret_client.columns[0:9]]
    row09 = csv_info_pret_client09.loc[int(id_client)].to_frame().T
    csv_info_pret_client014 = csv_info_pret_client[csv_info_pret_client.columns[8:14]]
    row014 = csv_info_pret_client014.loc[int(id_client)].to_frame().T
    return row09.to_dict("records"), row014.to_dict("records")


# callback: features pour graphique bi-variées (gauche)
@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown1_scatter_test_df', 'value'),
     Input('dropdown2_scatter_test_df', 'value'),
     Input('input_box_features', 'value'),
        ])
def update_scatter(drop1, drop2, id_client):
    if id_client is None:
        id_client = ID_CLIENT
    csv_features_imp_df = pd.read_csv(csv_features_imp_df_path)
    csv_features_imp_df = csv_features_imp_df.set_index("SK_ID_CURR")
    chart2 = px.scatter(data_frame=csv_features_imp_df,
                        x=drop1,
                        y=drop2,
                        color=csv_features_imp_df['SCORE_CLIENT'],
                        title=f"Graphique d'analyse {drop2} versus {drop1}",
                        height=500, )
    chart2.add_vline(x=csv_features_imp_df[drop1][id_client],
                     line_width=3, line_dash="dash", line_color="black",
                     annotation_text=f"Client {id_client}", annotation_font_size=14, annotation_font_color="black")
    chart2.add_hline(y=csv_features_imp_df[drop2][id_client],
                     line_width=3, line_dash="dash", line_color="black",
                     annotation_text=f"Client {id_client}", annotation_font_size=14, annotation_font_color="black")
    return chart2


# callback: features pour graphique histogram (droite)
@app.callback(
    Output('graph3', 'figure'),
    [Input('dropdown_bar_chart3', 'value'),
     Input('input_box_features', 'value'),
     ])
def update_bar(bar_drop, id_client):
    if id_client is None:
        id_client = ID_CLIENT
    csv_features_imp_df = pd.read_csv(csv_features_imp_df_path)
    csv_features_imp_df = csv_features_imp_df.drop(['Sexe', 'Niveau éducation', 'Statut familial'], axis=1)
    csv_features_imp_df = csv_features_imp_df.set_index("SK_ID_CURR")
    chart3 = px.histogram(data_frame=csv_features_imp_df,
                          x=bar_drop,
                          histnorm='percent',
                          color=csv_features_imp_df['PRED_CLASSE'],
                          barmode='overlay',
                          title=f"Distribution de {bar_drop} selon les classes",
                          height=500,
                          )
    chart3.add_vline(x=csv_features_imp_df[bar_drop][id_client],
                     line_width=3, line_dash="dash", line_color="black",
                    annotation_text=f"Client {id_client}", annotation_font_size=14, annotation_font_color="black"
                     )
    return chart3


if __name__ == '__main__':
    # connexion dashboard sur OVH, port internet=80
#    app.run_server(host="162.19.76.116", port=80)
    # connexion dashboard on local
    app.run_server(debug=True)

