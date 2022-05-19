from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests
import plotly.express as px
import pandas as pd
import json
from pathlib import Path

# version ID_CLIENT statique
ID_CLIENT = 103462
origin_path=Path('./')
temp_path = origin_path.joinpath('temp')
csv_info_pret_client_path = temp_path.joinpath('df_info_pret_client_500clients.csv')
csv_test_df_path = temp_path.joinpath('df_test_features_173_500clients.csv')


r_csv_info_pret = requests.get('http://127.0.0.1:5000/csv_info_pret_client/')
open(csv_info_pret_client_path, "wb").write(r_csv_info_pret.content)
csv_info_pret_client = pd.read_csv(csv_info_pret_client_path)


r_test = requests.get('http://127.0.0.1:5000/csv_df_test/')
open(csv_test_df_path, "wb").write(r_test.content)
csv_test_df = pd.read_csv(csv_test_df_path)
fig_features_fix = px.scatter(csv_test_df, x='PAYMENT_RATE', y='DAYS_EMPLOYED', size_max=8)

chart2 = px.scatter(data_frame=csv_test_df,
                    x=csv_test_df.columns[1],
                    y=csv_test_df.columns[2],
                    title=f"Scatter with features selection {csv_test_df.columns[2]} vs {csv_test_df.columns[1]}",
                    )

chart3 = px.bar(data_frame=csv_test_df,
               x="OBS_30_CNT_SOCIAL_CIRCLE",
               y=csv_test_df.columns[2],
               title=f"OBS_30_CNT_SOCIAL_CIRCLE vs {csv_test_df.columns[2]}",)



# figure de jauge sous plotly
fig_jauge = go.Figure()

ind= go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    # next value = score_client par rapport une proba_seuil de 47
    value = 30,
    mode = "gauge+number+delta",
    delta = {'reference': 47,
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
                            'thickness': 0.35, 'value': 47}})
fig_jauge.add_trace(ind)

fig_jauge.update_layout(paper_bgcolor='white',
                        height=200, width=300,
                        font={'color': 'darkblue', 'family': 'Arial'},
                        margin=dict(l=20, r=30, b=0, t=0, pad=0))



app = Dash(__name__)


dropdown1_scatter_test_df = dcc.Dropdown(
        id="dropdown1_scatter_test_df",
        options=[{"value":feature, "label":feature} for feature in csv_test_df.columns[1:]],
        value=csv_test_df.columns[1],
        clearable = False )


dropdown2_scatter_test_df = dcc.Dropdown(
        id="dropdown2_scatter_test_df",
        options=[{"value":feature, "label":feature} for feature in csv_test_df.columns[1:]],
        value=csv_test_df.columns[2],
        clearable = False )

dropdown_bar_chart3 = dcc.Dropdown(
        id="dropdown_bar_chart3",
        options=[{"value":label, "label":label} for label in csv_test_df.columns[1:]],
        value=csv_test_df.columns[1],
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

header = html.H2(children="Welcome to 👨 Gabriela's Dashboard ")

row1 = html.Div(children=[
    html.Img(src=app.get_asset_url('logo.png'), style={"display": "inline-block",
                                                       "width": "10%", }),
    html.Div(children=[
        html.H2("🏠 Projet 7: Implémentez un modèle de scoring"),
        dcc.Markdown(
            '''L’entreprise intitulé **Prêt à dépenser**, souhaite mettre en œuvre un **outil de “scoring crédit”** pour calculer la probabilité qu’un client rembourse son crédit, 
            puis classifie la demande en crédit accordé ou refusé. 
            L’entreprise souhaite développer un **algorithme de classification** en s’appuyant sur des sources de données variées 
            (données comportementales, données provenant d'autres institutions financières, etc.)
           Prêt à dépenser décide de développer un **dashboard interactif**  
           facilement exploitable par les chargés de relation client afin d’expliquer les décisions d’octroi de crédit, 
           et de disposer des informations clients à explorer facilement.''',
                     style={ 'white-space':'pre', 'fontSize': 20},),
    ], style={"display": "inline-block", "margin-left": "100px",  "width": "60%", }),

])

# Menu deroulant gauche pour obtenir info client!! attention!! seulement visualisation col21&22
col21 = html.Div(children=[
    html.H4("🔎 Selection ID Client"),
    dcc.Dropdown(csv_test_df.SK_ID_CURR, id='id_client_input', placeholder="Select Client Principal",
                 ),
    html.Br(),
    html.H4("📉 Jauge du Score Crédit ID Client", style={"background-color": "pink",}),
    dcc.Graph(figure=fig_jauge, id="my_jauge",),
], style={"border-style": "groove", 'display': 'inline-block', })

# Partie droite, Reponse du menu de gauche
col22 = html.Div(children=[
    html.H3('👁️ Client : Informations descriptives et demande de prêt :', style={"background-color": "pink",}),
    html.P('Selection du Client Principal:', style={"text-align": "left", "font-family": "Times New Roman"}),
    dcc.Dropdown(csv_info_pret_client.SK_ID_CURR,
                 id='id_client_info_input', placeholder="Select Client Principal",
                 style={"width": "40%"}),
    html.H3('Données personnelles du Client :', ),
    dash_table.DataTable(csv_info_pret_client.to_dict('records'),
                         [{"name": i, "id": i} for i in csv_info_pret_client.columns[1:9]],
                         style_header={'backgroundColor': '#cee1eb', "font-family": "Times New Roman",},
                         style_cell={'textAlign': 'center'},
                         style_data={'backgroundColor': '#cee1eb', "font-family": "Times New Roman",},
                         id='table1_info_client', ),
    html.Br(),
    html.H3('Données de la demande du crédit :', ),
    dash_table.DataTable(csv_info_pret_client.to_dict('records'),
                         [{"name": i, "id": i} for i in csv_info_pret_client.columns[9:14]],
                         style_header={'backgroundColor': '#cee1eb',"font-family": "Times New Roman",
                                       },
                         style_cell={'textAlign': 'center'},
                         style_data={'backgroundColor': '#cee1eb', "font-family": "Times New Roman",},
                         id='table2_info_client', ),
    html.Br(),
    html.H3('📉 Prediction Solvabilité du Client:', style={"background-color": "pink",}),
    dcc.Markdown(
        "La prédiction de la probabilité que le Client rembourse le crédit est calculé "
        "via une API spécifique avec LGBMClassifier, le meilleur modèle optimisé."
        "Pour le Client  {id_client} le score calculé via l’API est :  **{score_client}** \n "
        "L’algorithme de classification indique que la solvabilité du client est **{score_classe}** \n "
        "Le prêt est accordé au Client : **{score_text}**",
                 style={'white-space':'pre', 'fontSize': 18, "font-family": "Times New Roman",},
                 id='id_client_output_2',  ),
], style={'display': 'inline-block',
          "font-family": "Times New Roman", 'fontSize': 18,
          "margin-left": "200px",  "width": "55%",})

row2 = html.Div(children=[col21, col22,], style={'margin-bottom':'50px', 'text-align':'center'})


scatter_div= html.Div(children=[
    dropdown1_scatter_test_df, dropdown2_scatter_test_df, html.Br(),graph2 ],
    style={'display': 'inline-block', "width": "40%", "background-color": "#cee1eb",})

bar_div = html.Div(children=[dropdown_bar_chart3, html.Br(),graph3],
                   style={'display': 'inline-block',"width": "40%",
                          "margin-left": "70px", "background-color": "#cee1eb",} )

row3= html.Div(children=[scatter_div, bar_div, html.Br(), ],)

layout = html.Div(children=[row0, header, html.Hr(), row1, html.Hr(), row2,html.Br(), html.Hr(), row3, html.Br(), html.Hr(),],
                  style={"text-align": "center","background-color": "#cee1eb",
                         "font-family": "Times New Roman",})




app.layout = layout


# callback: IDclient --figure jauge -- score client
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


# callback: retour de prediction score client en affichage text
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
        score_text = "NON"
    else:
        score_text = "Oui"
    return f'''
            La prédiction de la probabilité que le Client rembourse le crédit est calculé via une API spécifique avec LGBMClassifier, le meilleur modèle optimisé. 
            Pour le Client  {id_client} le score calculé via l’API est :  **{score_client}**
            L’algorithme de classification indique que la solvabilité du client est **{score_classe}**
            Le prêt est accordé au Client : **{score_text}**'''


# callback: bouton id_client - 2 tables de 1 ligne avec info cleint et prêt
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


@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown1_scatter_test_df', 'value'),
     Input('dropdown2_scatter_test_df', 'value')])
def update_scatter(drop1, drop2):
    chart2 = px.scatter(data_frame=csv_test_df,
                   x=drop1,
                   y=drop2,
                   title=f"Scatter with features selection {drop2} vs {drop1}",
                   height=500,)
    return chart2


@app.callback(
    Output('graph3', 'figure'),
    [Input('dropdown_bar_chart3', 'value')])
def update_bar(bar_drop):
    chart3 = px.bar(data_frame=csv_test_df,
               x="OBS_30_CNT_SOCIAL_CIRCLE",
               y=bar_drop,
               title=f"OBS_30_CNT_SOCIAL_CIRCLE vs {csv_test_df.columns[2]}",
               height=500,
               )
    return chart3


if __name__ == '__main__':
    app.run_server(debug=True)


