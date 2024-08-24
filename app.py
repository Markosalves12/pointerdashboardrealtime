import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from routs import (get_daily_activity, get_route_history,
                             get_vehicles_info, login_rout, params, url_base, account_administration_rout,
                             get_vehicle_groups, get_vehicles,
                             vehicle_management_rout, get_drivers,
                             driver_rout)

from class_time_format import converte_to_seconds__hh_mm_ss
from class_create_graphs import CreatGraphs
from class_api import ApiPointer
from class_account_administration import AccountAdministration
from class_convert_account_administration import ConvertAccountAdministration
from class_vehicle_management import VehicleManagement
from class_convert_vehicle_management import ConvertVehicleManagement
from class_driver_management import DriverManagement
from class_convert_driver_management import ConvertDriverManagement
from class_Calendar import Calendar, datas_unicas_formato_string
from class_image import Image
from class_send_email import SendEmail

import locale
from datetime import datetime

login = ApiPointer(url=url_base, user_name=params['login'], password=params['senha'])
token = login.login(login_rout)

account_administration = AccountAdministration(url=url_base, rout=account_administration_rout,
                                               token_for_access=token, verify=False)
getvehiclesgroups = account_administration.get_accounts(second_rout=get_vehicle_groups)
GetVehicleGroup = ConvertAccountAdministration(validation=True).convert_get_vehicle_groups(getvehiclesgroups)
vehicle_management = VehicleManagement(url=url_base,
                                       rout=vehicle_management_rout, token_for_access=token, verify=False)
getvehicles = vehicle_management.get_vehicles(get_vehicles)
GetVehicles = ConvertVehicleManagement(validation=True).convert_get_vehicles(getvehicles)
driver_management = DriverManagement(url=url_base, rout=driver_rout, token_for_access=token, verify=False)
drivers = driver_management.get_drivers(second_rout=get_drivers)
GetDrivers = ConvertDriverManagement(validation=True).convert_get_drivers(drivers)
calendario = Calendar(dia=1, mes=9, ano=2022, dia_final=31, mes_final=12, ano_final=2024).formatar_calendario()



datas_daily_activities, datas_rout_history = datas_unicas_formato_string(dataframe=calendario, datas='Dia',
                                                                         mes='Setembro', ano='2023')
get_daily_activies = vehicle_management.get_daily_activity(second_rout=get_daily_activity,
                                                           licenseplate='RGC2D78',
                                                           vehicleids='185531',
                                                           dates=datas_daily_activities)

GetDailyActivities = ConvertVehicleManagement(validation=True).convert_get_daily_activity(get_daily_activies)

get_history_activies = vehicle_management.get_route_history(second_rout=get_route_history,
                                                            licenseplate='RGC2D78',
                                                            vehicleids='185531',
                                                            dates=datas_daily_activities,
                                                            hour1=5,
                                                            hour2=15)

GetRoutHistory = ConvertVehicleManagement(validation=True).convert_get_rout_history(get_history_activies)

get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                       licenseplate=['RGC2D78'],
                                                       vehicleids=['185531'])
GetVehicleInfo = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)

temporary_drivers = GetDrivers.rename(columns={'Id': 'DriverId'})
filtered_addresses = pd.merge(GetRoutHistory, temporary_drivers,
                              on='DriverId', how='left')

filtered_addresses['Motorista'] = filtered_addresses['Motorista'].astype(str)
filtered_addresses['Endereco'] = filtered_addresses['Endereco'].fillna('Não identificado')

options_drivers = ([{'label': 'Selecionar Tudo', 'value': 'Todos'}]
                   + [{'label': motorista, 'value': motorista} for
                      motorista in filtered_addresses['Motorista'].unique()])

tipo_dias_options = ([{'label': 'Selecionar Tudo', 'value': 'Todos'}]
                     + [{'label': tipo_de_dia, 'value': tipo_de_dia} for
                        tipo_de_dia in calendario['Tipo de Dia'].unique()])

dias_options = calendario[(calendario['Mês'] == "Setembro") & (calendario['Ano'] == '2023')]['Número do Dia'].unique()

# Configura a localização para português do Brasil ('pt_BR')
locale.setlocale(locale.LC_TIME, 'pt_BR')

codigo = 0
update_tela = False


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH], title="Telemetria")
server = app.server

tela_login = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    html.Div(
                        html.Iframe(
                            srcDoc=Image(path_svg=r"logo facilities (1).svg").open_image(),
                            width=f"100%", height=f"110%",
                        ), style={'justify-content': 'center'}
                    ),
                ),
                html.P(),
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input(placeholder='Endereço de E-Mail', style={'width': '100%'},
                                          id='email-to-verify'),
                                html.P(),
                                html.P(),
                            ],
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input(placeholder='Código de verificação', style={'width': '100%'},
                                          id='code-to-verify', disabled=True),
                                html.P(),
                                html.P(),
                            ],
                        ),
                    ], id='Check-Code'
                ),
                dbc.Row(
                    children = dbc.Button(
                        "Enviar Código", n_clicks=0, className="btn btn-outline-primary",
                        id='verify-email'
                    ), id='button-verify-email'
                )
            ], style={'justify-content': 'center'}
        ),
    ], style={'justify-content': 'center'}
)

tab_historico_percurso = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        html.P(),
                        dbc.Col(
                            children=[dcc.Dropdown(GetVehicleGroup['Name'].unique(),
                                                   value='Unidade Mucuri',
                                                   id='dropdown-vehicle-group', placeholder='Unidades')],
                            width=1,
                            style={'fontSize': 12},
                        ),
                        dbc.Col(
                            # value=random.choice(GetVehicles['LicencePlate'].unique())
                            children=[dcc.Dropdown(GetVehicles['LicencePlate'].unique(),
                                                   value='QXI7205',
                                                   id='dropdown-LicencePlate', placeholder='Placa'), ],
                            width=1,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    options=[
                                        {'label': 'Selecionar Tudo', 'value': 'Todos'},
                                        {'label': 'Ligado', 'value': 'Ligado'},
                                        {'label': 'Desligado', 'value': 'Desligado'}
                                    ],
                                    value='Todos',
                                    multi=False,
                                    id='dropdown-enginie_status',
                                    placeholder='Status Motor'
                                )
                            ],
                            width=2,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    options=[{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
                                        {'label': endereco, 'value': endereco} for endereco in
                                        filtered_addresses['Endereco'].unique()],
                                    multi=False,  # Permite seleção múltipla
                                    id='dropdown-adress',
                                    placeholder='Endereço'
                                )
                            ],
                            width=2,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    options=[{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
                                        {'label': endereco, 'value': endereco} for endereco in
                                        filtered_addresses['Motorista'].unique()],
                                    multi=False,
                                    id='dropdown-driver-name',
                                    placeholder='Motorista'
                                ),
                            ],
                            width=2,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[dcc.Dropdown(tipo_dias_options, id='dropdown-tipo-dia',
                                                   placeholder='Tipo de dia'), ],
                            width=1,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[dcc.Dropdown(dias_options, value='01', id='dropdown-dia', placeholder='Dia'), ],
                            width=1,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[dcc.Dropdown(calendario['Mês'].unique(), value='Setembro', id='dropdown-mes',
                                                   placeholder='Mês'), ],
                            width=1,
                            style={'fontSize': 12}
                        ),
                        dbc.Col(
                            children=[dcc.Dropdown(calendario['Ano'].unique(), value='2023', id='dropdown-ano',
                                                   placeholder='Ano'), ],
                            width=1,
                            style={'fontSize': 12}
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.P(),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Velocidade máxima", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-velocidade-máxima")),
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Distância total", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-distancia-total"))
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Distância máxima", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-distancia-máxima"))
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Distância média", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-distancia-média"))
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Tempo máximo em direção", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-tempo-máximo"))
                                            ]
                                        )
                                    ],
                                )
                            ],
                        ),
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H6("Tempo médio em direção", className="card-subtitle"),
                                                html.Strong(html.P(className="card-text", id="card-tempo-médio"))
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.P(),
                        dbc.Col(
                            dbc.Row(
                                children=[dcc.RangeSlider(0, 23, 1, value=[5, 15], id='hours_range')]
                            ), width=12,
                        ),
                        html.P(),
                    ],
                ),
                dbc.Row(
                    [
                        html.P(),
                        dbc.Col(
                            [
                                dbc.Row(
                                    children=[dcc.Graph(id="distance-day", figure={}, style={'width': '100%'})],
                                ),
                                dbc.Row(
                                    children=[dcc.Graph(id="time-day", figure={}, style={'width': '100%'})],
                                ),
                            ], width=6,
                        ),
                        dbc.Col(
                            children=[dcc.Graph(id="Grafico aleatorio", figure={}, style={'width': '100%'})
                                      ], width=3,
                        ),
                        dbc.Col(
                            children=[dcc.Graph(id="vehicle-positions", figure={}, style={'width': '100%'})
                                      ], width=3,
                        )
                    ],
                )
            ], style={'width': '100%'}
        )
    ], style={'width': '100%'}
)

real_time_monitoring = html.Div(
    [
        html.Div(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.P(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(),
                                dbc.Col(
                                    children=[dcc.Dropdown(GetVehicleGroup['Name'].unique(),
                                                           value='Unidade Mucuri',
                                                           id='dropdown-vehicle-group-real-time',
                                                           placeholder='Unidade'), ],
                                    width=1,
                                    style={'fontSize': 12}
                                ),
                                dbc.Col(
                                    # value=random.choice(GetVehicles['LicencePlate'].unique())
                                    children=[dcc.Dropdown(GetVehicles['LicencePlate'].unique(),
                                                           value='QXI7205',
                                                           id='dropdown-LicencePlate-real-time',
                                                           placeholder='Placa'), ],
                                    width=1,
                                    style={'fontSize': 12}
                                ),
                                # html.P(),
                            ],
                        ),
                        dbc.Row(
                            [
                                html.P(),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Ultima atualização",
                                                                className="card-subtitle"),
                                                        html.Strong(
                                                            html.P(className="card-text", id="card-last-update"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Ultima transmissão", className="card-subtitle"),
                                                        html.Strong(
                                                            html.P(className="card-text", id="card-last-transmission"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Motorista", className="card-subtitle"),
                                                        html.Strong(
                                                            html.P(className="card-text", id="card-driver-name"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Velocidade", className="card-subtitle"),
                                                        html.Strong(html.P(className="card-text", id="card-speed"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Endereço", className="card-subtitle"),
                                                        html.Strong(html.P(className="card-text", id="card-adress"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ], width=3
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H6("Status de ignição", className="card-subtitle"),
                                                        html.Strong(html.P(className="card-text", id="card-ignition"))
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                html.P(),
                                dbc.Col(
                                    dbc.Row(
                                        children=[dcc.RangeSlider(0, 23, 1, value=[0, 15], id='hours_range-real-time')]
                                    ), width=12
                                ),
                                html.P(),
                                html.P(),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[dcc.Graph(id='activies-today',
                                                        config={'displayModeBar': False},
                                                        # Oculta a barra de modo de exibição
                                                        style={'width': '100%'}), ], width=6,

                                ),
                                dbc.Col(
                                    children=[dcc.Graph(id='Positions-today',
                                                        config={'displayModeBar': False},
                                                        style={'width': '100%'})], width=6,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        dcc.Interval(
            id='interval-component-cards',
            interval=10 * 1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-component-map',
            interval=5 * 60 * 1000,
            n_intervals=0
        ),
    ], style={'width': '100%'}
)

real_time_monitoring_all_vehicles = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                html.P(),
                                dbc.Col(
                                    children=[dcc.Dropdown(
                                        options=[{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
                                    {'label': unidade, 'value': unidade} for unidade in
                                        GetVehicleGroup['Name'].unique()],
                                        value='Unidade Mucuri',
                                        id='dropdown-select-all-vehicle-group', placeholder='Unidades', clearable=False)],
                                    width= 2,
                                    style={'fontSize': 12},
                                ),
                                dbc.Col(
                                    # value=random.choice(GetVehicles['LicencePlate'].unique())
                                    children=[dcc.Dropdown(
                                    options=[{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
                                    {'label': placa, 'value': placa} for placa in
                                        GetVehicles['LicencePlate'].unique()],
                                        value=['Todos'],
                                        id='dropdown-select-all-LicencePlate',
                                        placeholder='Placa', multi=True),],
                                    width=8,
                                    style={'fontSize': 12},
                                ),
                                dbc.Col(
                                    children=[
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'Selecionar Tudo', 'value': 'Todos'},
                                                {'label': 'Ligado', 'value': 'Ligado'},
                                                {'label': 'Desligado', 'value': 'Desligado'}
                                            ],
                                            value='Todos',
                                            multi=False,
                                            id='dropdown-enginie_status-all-vehicle',
                                            placeholder='Status Motor'
                                        )
                                    ],
                                    width=2,
                                    style={'fontSize': 12}
                                ),
                            ]
                        ),
                        dbc.Row(
                                [
                                    html.P(),
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardBody(
                                                        [
                                                            html.H6("Frota ativa", className="card-subtitle"),
                                                            html.Strong(html.P(className="card-text", id="card-vehicles-activies"))
                                                        ]
                                                    )
                                                ],
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardBody(
                                                        [
                                                            html.H6("Motoristas autenticadas", className="card-subtitle"),
                                                            html.Strong(html.P(className="card-text", id="card-drivers-authenticates"))
                                                        ]
                                                    )
                                                ],
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardBody(
                                                        [
                                                            html.H6("Veículos ligados", className="card-subtitle"),
                                                            html.Strong(
                                                                html.P(className="card-text", id="card-vehicles-on"))
                                                        ]
                                                    ),
                                                ],
                                            )
                                        ]
                                    ),
                                    html.P()
                                ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[dcc.Graph(figure={}, id='activies-today-all-vehicle')],
                                    width=5
                                ),
                                dbc.Col(
                                    children=[dcc.Graph(figure={}, id='positions-today-all-vehicle')],
                                    width=7
                                )
                            ],
                        )
                    ],
                )
            ],  style={'width': '100%'}
        )
    ], style={'width': '100%'}
)

# Layout do aplicativo
paineis = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.Iframe(
                            srcDoc=Image(path_svg=r"logo facilities.svg").open_image(),
                            width=f"500", height=f"100"
                        ),
                    ), width=3
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4(children=f"Sistema de telemetria pointer"),
                        ),
                        dbc.Row(
                            html.H4(children=f"Desenvolvido por Facilities Suzano")
                        ),
                        dbc.Row(
                            html.H4(children=f"V0.1 Beta (teste) Atualizado"
                                             f"em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", id='dummy-output'),
                        )
                    ]
                )
            ]
        ),
        dbc.Tabs(
            [
                dbc.Tab(tab_historico_percurso, label="Hitórico de percurso"),
                dbc.Tab(real_time_monitoring, label="Real Time"),
                dbc.Tab(real_time_monitoring_all_vehicles, label="Todos os veículos")
            ]
        ),
        dcc.Interval(
            id='interval-component-update-databases',
            interval=1 * 40 * 60 * 1000,
            n_intervals=0
        ),
    ]
)


app.layout = html.Div(
    [
        html.Div(
            children=dbc.Row(
                [
                    tela_login
                ], id='tela inicial'
            ), id='principal-screen'
        ),
        dcc.Interval(
            id='interval-component-logscreen',
            interval=5*60*60*1000,
            n_intervals=0
        )
    ],
)


# Atualizar a cor e a mensagem do botão ao clicar
@app.callback(
    [Output('button-verify-email', 'children'),
    Output('Check-Code', 'children'),
    Input('verify-email', 'n_clicks'),
    State('email-to-verify', 'value'),
    State('code-to-verify', 'value'),]
)

def verify_email(n_clicks, email, code):
    global codigo, update_tela
    prevent_codigo = codigo

    email = str(email).lower().strip()
    verify_code = dbc.Col(
            [
                dbc.Input(placeholder='Código de verificação', style={'width': '100%'},
                          id='code-to-verify', disabled=True),
                html.P(),
                html.P(),
            ],
        ),

    if n_clicks == 0:
        resend = dbc.Button(
            "Enviar Código", n_clicks=0, className="btn btn-outline-primary",
            id='verify-email'
        )

        return resend, verify_code

    if  n_clicks > 0  and '@suzano.com' not in email:
        resend = dbc.Button(
            "Digite um E-Mail válido", n_clicks=0, className="btn btn-outline-danger",
            id='verify-email'
        ),

        return resend, verify_code

    if n_clicks > 0 and '@suzano.com' in email and code != None:
        if code == codigo:
            update_tela = True
            codigo = SendEmail(para=None).create_codigo()
            raise PreventUpdate
        else:
            raise PreventUpdate


    if n_clicks > 0  and '@suzano.com' in email and codigo == prevent_codigo:
        resend = dbc.Button(
            "Digite seu código de acesso", n_clicks=1, className="btn btn-outline-success",
            id='verify-email'
        ),

        verify_code = dbc.Col(
                [
                    dbc.Input(placeholder='Código de verificação', style={'width': '100%'},
                              id='code-to-verify', disabled=False),
                    html.P(),
                    html.P(),
                ],
            ),
        codigo = SendEmail(para=email).send_email()
        return resend, verify_code



@app.callback(
    Output('tela inicial', 'children'),
    Input('verify-email', 'n_clicks')
)

def update_tela(n_clicks):
    global update_tela, codigo
    if n_clicks > 0 and update_tela == True:
        tela = [
            paineis
        ]

        return tela

    else:
        raise PreventUpdate



@app.callback(
    Output('principal-screen', 'children'),
    Input('interval-component-logscreen', 'n_intervals')
)
def relog(n_intervals):
    global update_tela
    update_tela = False
    tela = dbc.Row(
                [
                    tela_login
                ], id='tela inicial'
            ),

    return tela


""" Callback da página Histíco de percurso """

# #Calback que faz a seleção de mes variar conforme a seleçao do ano
# #Desabilitada temporariamente por Bugs na atualização automatica do calendario
# @app.callback(
#     Output('dropdown-mes', 'options'),
#     Input('dropdown-ano', 'value')
# )
# def update_month_options(selected_ano):
#     month_options = calendario[calendario['Ano'] == selected_ano]['Mês'].unique()
#     return month_options


#Callback que mantem a seleção de dias coerente
#para fins de semana e para anos bissextos
@app.callback(
    Output('dropdown-dia', 'options'),
    Input('dropdown-ano', 'value'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-tipo-dia', 'value')
)
def update_day_options(selected_ano, selected_mes, selected_tipo_de_dia):
    if selected_tipo_de_dia and selected_tipo_de_dia != 'Todos':
        temp_calendario = calendario[calendario['Tipo de Dia'] == selected_tipo_de_dia]
        dias_options = temp_calendario[(temp_calendario['Mês'] == selected_mes)
                                       & (temp_calendario['Ano'] == selected_ano)
                                       & (temp_calendario['Tipo de Dia'] == selected_tipo_de_dia)
                                       ]['Número do Dia'].unique()

        return dias_options

    dias_options = calendario[(calendario['Mês'] == selected_mes) & (calendario['Ano'] == selected_ano)][
        'Número do Dia'].unique()

    return dias_options


#Calback que mantem a opção de placas coerente de acordo com a seleção da carteira de veículos
@app.callback(
    Output('dropdown-LicencePlate', 'options'),
    Input('dropdown-vehicle-group', 'value')
)
def update_licence_plate_options(selected_group):
    filtered_vehicles_group_id = list(GetVehicleGroup[GetVehicleGroup['Name'] == selected_group]['Id'].unique())
    filtered_vehicles = GetVehicles[GetVehicles['GroupId'].isin(filtered_vehicles_group_id)]
    options = [{'label': placa, 'value': placa} for placa in filtered_vehicles['LicencePlate'].unique()]
    return options

#Calback que mantem os visuais Distancia percorrida por dia e tempo de direção por dia
#Calback que mantem os cartões atualizados
@app.callback(
    # cards com os princiapis indicadores referentes aos filtros especificados
    Output('card-velocidade-máxima', 'children'),
    Output('card-distancia-total', 'children'),
    Output('card-distancia-máxima', 'children'),
    Output("card-distancia-média", 'children'),
    Output("card-tempo-máximo", 'children'),
    Output("card-tempo-médio", 'children'),
    # Graficos de barras com a distancia por dia e tempo por dia
    Output("distance-day", 'figure'),
    Output("time-day", 'figure'),
    # dropdowns de seleção
    Input('dropdown-LicencePlate', 'value'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-ano', 'value'),
    Input('dropdown-tipo-dia', 'value'),
    # Os visuais atualizam junto com as bases de dados
    Input('interval-component-update-databases', 'n_intervals')
)
def update_dropdowns_cards_bar_graphs(selected_licence_plate, selected_mes,
                                      selected_ano, selected_tipo_de_dia, n_interval):
    # função que retorna visuais em branco caso algun filro obbrigatório não seja especificado
    def return_blanck():
        max_speed = "Sem dados"
        total_distance = "Sem dados"
        max_distance = "Sem dados"
        avg_distance = "Sem dados"
        max_time = "Sem dados"
        avg_time = "Sem dados"

        data = {'dia': list(range(1, 32)),
                'Distancia': [0] * 31,
                'Segundos de direcao': [0] * 31,
                'Tempo de direcao': ['00:00:00'] * 31}
        df = pd.DataFrame(data)

        barras_distance_day = CreatGraphs(data_frame=df, height=300, margin=dict(l=0, r=0, t=27, b=0),
                                          size=10, title='Distância percorrida por dia',
                                          x='dia', y='Distancia').create_bar_chart(label_column='Distancia')

        barras_time_day = CreatGraphs(data_frame=df, height=300, margin=dict(l=0, r=0, t=27, b=0),
                                      size=10, title='Tempo de direção por dia',
                                      x='dia', y='Segundos de direcao').create_bar_chart(
            label_column='Tempo de direcao')

        return (max_speed, total_distance,
                max_distance, avg_distance, max_time, avg_time,
                barras_distance_day, barras_time_day)

    #Caso o filtro de placa fique em branco os visuais tbm ficam em branco automaticamente
    if selected_licence_plate == "" or selected_licence_plate == None:
        (max_speed, total_distance, max_distance, avg_distance, max_time, avg_time,
         barras_distance_day, barras_time_day) = return_blanck()

        return (max_speed, total_distance, max_distance, avg_distance, max_time, avg_time,
                barras_distance_day, barras_time_day)

    temp_calendar = calendario

    #caso o filtro tipo de dia seja branco retona integralmente os dados do periodo selecionado
    #tipo de dia = fim de semana/dia ultil
    if selected_tipo_de_dia and selected_tipo_de_dia != 'Todos':
        temp_calendar = calendario[calendario['Tipo de Dia'] == selected_tipo_de_dia]

    vehicle_id = GetVehicles[GetVehicles['LicencePlate'] ==
                             selected_licence_plate]['VehicleId'].unique()[0]

    datas_daily_activities, datas_rout_history = (datas_unicas_formato_string
                                                  (dataframe=temp_calendar, datas='Dia',
                                                   mes=selected_mes, ano=f'{selected_ano}'))

    getdailyactivies = vehicle_management.get_daily_activity(second_rout=get_daily_activity,
                                                               licenseplate=selected_licence_plate,
                                                               vehicleids=f'{vehicle_id}',
                                                               dates=datas_daily_activities)

    Get_Daily_Activities = ConvertVehicleManagement(validation=True).convert_get_daily_activity(getdailyactivies)

    #caso a tabela gerada seja maior que 0 linhas, siginifica que ha dados nos filtros selecionados
    if len(Get_Daily_Activities) > 0:
        max_speed = f"{Get_Daily_Activities['Velocidade Maxima'].max()} Km/H"
        total_distance = f"{Get_Daily_Activities['Distancia'].sum()} Km"
        max_distance = f"{Get_Daily_Activities['Distancia'].max()} Km"
        avg_distance = "{:.2f}".format(Get_Daily_Activities['Distancia'].sum() / len(Get_Daily_Activities)) + " Km"
        max_time = f"{Get_Daily_Activities['Tempo de direcao'].max()}"
        avg_time = f"{converte_to_seconds__hh_mm_ss(int(Get_Daily_Activities['Segundos de direcao'].sum() / len(Get_Daily_Activities)))}"

        barras_distance_day = CreatGraphs(data_frame=Get_Daily_Activities, height=300, margin=dict(l=0, r=0, t=27, b=0),
                                          size=10, title='Distância percorrida por dia',
                                          x='dia', y='Distancia').create_bar_chart(label_column='Distancia',
                                                                                       bar_color='#0044B2',
                                                                                       background_color='#ffffff')

        barras_time_day = CreatGraphs(data_frame=Get_Daily_Activities, height=300, margin=dict(l=0, r=0, t=27, b=0),
                                      size=10, title='Tempo de direção por dia',
                                      x='dia', y='Segundos de direcao').create_bar_chart(
            label_column='Tempo de direcao',
            bar_color='#00C85A',
            background_color='#ffffff')

        return (max_speed, total_distance,
                max_distance, avg_distance, max_time, avg_time,
                barras_distance_day, barras_time_day)

    # caso a tabela gerada seja igual a 0, significa que não ha dados no periodo selecionado, retorna os visuais em branco tbm
    else:
        (max_speed, total_distance, max_distance, avg_distance, max_time, avg_time,
         barras_distance_day, barras_time_day) = return_blanck()

        return (max_speed, total_distance, max_distance, avg_distance,
                max_time, avg_time, barras_distance_day, barras_time_day)

#Callback que mantem a tabela e o mapa atualizados de acorod com o filtro especificado
@app.callback(
    # a consulta tambem atualiza as possiveis seleções dos dropdowns,
    # de endereço e nome do motorista
    Output('dropdown-adress', 'options'),
    Output('dropdown-driver-name', 'options'),
    # Visuais com a tabela e o mapa
    Output("vehicle-positions", 'figure'),
    Output("Grafico aleatorio", 'figure'),
    # Dropdowns que filtram a seleção
    Input('dropdown-LicencePlate', 'value'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-ano', 'value'),
    Input('dropdown-dia', 'value'),
    Input('hours_range', 'value'),
    Input('dropdown-enginie_status', 'value'),
    Input('dropdown-adress', 'value'),
    Input('dropdown-driver-name', 'value'),
    # Os visuais atualizam junto com as bases de dados
    Input('interval-component-update-databases', 'n_intervals')
)
def update_table_maps(selected_licence_plate, selected_mes, selected_ano,
                      selected_dia, selected_hours, selected_engine_status,
                      selected_address, selected_driver_name, n_intervals):

    def return_blancks():
        filtered_addresses = pd.DataFrame(
            {
                'Data Hora': [], 'Endereco': [], 'Motorista': [], 'Lat': [], 'Long': []
            }
        )

        options_adress = [{'label': 'Selecionar Tudo', 'value': 'Todos'}]

        options_drivers = [{'label': 'Selecionar Tudo', 'value': 'Todos'}]

        map_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                    margin=dict(l=0, r=0, t=0, b=0), size=10,
                                    title="Posições do veiculo",
                                    x='Lat', y='Long').creat_map_box_blanck(zoom=10, mapbox_style='open-street-map')

        table_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                      margin=dict(l=0, r=15, t=0, b=0), size=10,
                                      title="Posições do veiculo",
                                      x='Lat', y='Long').create_table_blank(
            columns=['Data Hora', 'Endereco', 'Motorista'])

        return (options_adress, options_drivers, map_positions, table_positions)

    if selected_licence_plate == '' or selected_licence_plate == None:
        options_adress, options_drivers, map_positions, table_positions = return_blancks()
        return options_adress, options_drivers, map_positions, table_positions

    vehicle_id = GetVehicles[GetVehicles['LicencePlate'] == selected_licence_plate]['VehicleId'].unique()[0]

    temp_calendar = calendario[
        (calendario['Mês'] == selected_mes) & (calendario['Ano'] == selected_ano)
        & (calendario['Número do Dia'] == selected_dia)
        ]

    datas_daily_activities, datas_rout_history = datas_unicas_formato_string(dataframe=temp_calendar,
                                                                             datas='Dia',
                                                                             mes=selected_mes,
                                                                             ano=f'{selected_ano}')

    get_history_activies = vehicle_management.get_route_history(second_rout=get_route_history,
                                                                licenseplate=selected_licence_plate,
                                                                vehicleids=f'{vehicle_id}',
                                                                dates=datas_daily_activities,
                                                                hour1=selected_hours[0],
                                                                hour2=selected_hours[1])

    filtered_addresses = ConvertVehicleManagement(validation=True).convert_get_rout_history(get_history_activies)

    # filtered_addresses = filtered_addresses[(filtered_addresses['Hora'] >= selected_hours[0])
    #                                         & (filtered_addresses['Hora'] <= selected_hours[1])]

    if selected_engine_status and selected_engine_status != 'Todos':
        filtered_addresses = filtered_addresses[filtered_addresses['Iginicao'] == selected_engine_status]

    if selected_address and selected_address != 'Todos':
        filtered_addresses = filtered_addresses[filtered_addresses['Endereco'] == selected_address]

    if selected_driver_name and selected_driver_name != 'Todos':
        filtered_addresses = filtered_addresses[filtered_addresses['Motorista'] == selected_driver_name]

    temporary_drivers = GetDrivers[['Id', 'Nome Motorista']].rename(columns={'Id': 'DriverId'})
    filtered_addresses = pd.merge(filtered_addresses, temporary_drivers,
                                  on='DriverId', how='left')

    filtered_addresses['Motorista'] = filtered_addresses['Motorista'].astype(str)
    filtered_addresses['Endereco'] = filtered_addresses['Endereco'].fillna('Não identificado')

    if len(filtered_addresses) > 0:
        options_adress = [{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [{'label': endereco, 'value': endereco} for
                                                                             endereco in
                                                                             filtered_addresses['Endereco'].unique()]

        options_drivers = [{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [{'label': motorista, 'value': motorista}
                                                                              for motorista in
                                                                              filtered_addresses['Motorista'].unique()]

        map_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                    margin=dict(l=0, r=0, t=0, b=0), size=10,
                                    title="Posições do veiculo",
                                    x='Lat', y='Long').create_map_box(hover_name='Endereco', zoom=10,
                                                                      mapbox_style='open-street-map',
                                                                      hover_data=['Endereco',
                                                                                  'Motorista',
                                                                                  'Data Hora',
                                                                                  'Tipo de sinal'])

        table_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                      margin=dict(l=0, r=15, t=0, b=0), size=10,
                                      title="Posições do veiculo",
                                      x='Lat', y='Long').create_table(columns=['Data Hora',
                                                                               'Endereco', 'Motorista'])

        return (options_adress, options_drivers, map_positions, table_positions)

    else:
        options_adress, options_drivers, map_positions, table_positions = return_blancks()
        return options_adress, options_drivers, map_positions, table_positions


@app.callback(
    Output('dropdown-LicencePlate-real-time', 'options'),
    Input('dropdown-vehicle-group-real-time', 'value')
)
def update_licence_plate_options(selected_group):
    filtered_vehicles_group_id = list(GetVehicleGroup[GetVehicleGroup['Name'] == selected_group]['Id'].unique())
    filtered_vehicles = GetVehicles[GetVehicles['GroupId'].isin(filtered_vehicles_group_id)]
    options = [{'label': placa, 'value': placa} for placa in filtered_vehicles['LicencePlate'].unique()]
    return options


@app.callback(
    Output('card-last-update', 'children'),
    Output('card-last-transmission', 'children'),
    Output('card-driver-name', 'children'),
    Output('card-speed', 'children'),
    Output('card-adress', 'children'),
    Output('card-ignition', 'children'),
    Input('dropdown-LicencePlate-real-time', 'value'),
    Input('interval-component-cards', 'n_intervals'),
)
def update_cards_realtime(selected_licence_plate, n_intervals):
    def return_blancks():
        last_update = "Selecione uma placa/unidade"
        last_transmission = "Selecione uma placa/unidade"
        driver_name = "Selecione uma placa/unidade"
        speed = "Selecione uma placa/unidade"
        adress = "Selecione uma placa/unidade"
        ignition = "Selecione uma placa/unidade"

        return last_update, last_transmission, driver_name, speed, adress, ignition

    if selected_licence_plate == '' or selected_licence_plate == None:
        last_update, last_transmission, driver_name, speed, adress, ignition = return_blancks()
        return last_update, last_transmission, driver_name, speed, adress, ignition

    vehicle_id = GetVehicles[GetVehicles['LicencePlate'] == selected_licence_plate]['VehicleId'].unique().astype(str)


    get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                           licenseplate=[selected_licence_plate],
                                                           vehicleids=vehicle_id)



    GetVehicleInfo = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)

    if len(GetVehicleInfo) > 0:
        last_update = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        last_transmission = f"{GetVehicleInfo['Ultima Menssagem'].unique()[0]}"
        driver_name = f"{GetVehicleInfo['Motorista'].unique()[0]}"
        speed = f"{GetVehicleInfo['Velocidade'].unique()[0]}"
        adress = f"{GetVehicleInfo['Endereco'].unique()[0]}"
        ignition = f"{GetVehicleInfo['Ignicao'].unique()[0]}"

        return last_update, last_transmission, driver_name, speed, adress, ignition

    else:
        last_update, last_transmission, driver_name, speed, adress, ignition = return_blancks
        return last_update, last_transmission, driver_name, speed, adress, ignition


@app.callback(
    Output('Positions-today', 'figure'),
    Output('activies-today', 'figure'),
    Input('dropdown-LicencePlate-real-time', 'value'),
    Input('hours_range-real-time', 'value'),
    Input('interval-component-map', 'n_intervals'),
)
def update_maps_real_time(selected_licence_plate, selected_hours, n_intervals):
    def return_blancks():
        blanck_data = pd.DataFrame(
            {
                'Lat': [], 'Long': [], 'Data Hora': [], 'Endereco': [],
                'Motorista': [], 'Ignicao': []
            }
        )
        map_positions_black = CreatGraphs(data_frame=blanck_data, height=600,
                                          margin=dict(l=0, r=0, t=0, b=0), size=10,
                                          title="Posições do veiculo",
                                          x='Lat', y='Long').creat_map_box_blanck(zoom=3,
                                                                                  mapbox_style='open-street-map')

        table_positions_blanck = CreatGraphs(data_frame=blanck_data, height=600,
                                             margin=dict(l=0, r=15, t=0, b=0), size=10,
                                             title="Posições do veiculo",
                                             x='Lat', y='Long').create_table_blank(
            columns=['Data Hora', 'Endereco', 'Motorista', 'Ignicao'])

        return map_positions_black, table_positions_blanck

    if selected_licence_plate == "" or selected_licence_plate == None:
        map_positions, table_positions = return_blancks()

        return map_positions, table_positions

    vehicle_id = GetVehicles[GetVehicles['LicencePlate'] == selected_licence_plate]['VehicleId'].unique()[0]

    selected_mes = str(datetime.now().strftime("%B")).title()
    selected_ano = datetime.now().strftime("%Y")
    selected_dia = datetime.now().strftime("%d")


    calendar_dates = calendario[
        (calendario['Mês'] == selected_mes) & (calendario['Ano'] == selected_ano)
        & (calendario['Número do Dia'] == selected_dia)
        ]


    datas_daily_activities, datas_rout_history = datas_unicas_formato_string(dataframe=calendar_dates,
                                                                             datas='Dia',
                                                                             mes=f'{selected_mes}',
                                                                             ano=f'{selected_ano}')


    get_history_activies = vehicle_management.get_route_history(second_rout=get_route_history,
                                                                licenseplate=selected_licence_plate,
                                                                vehicleids=f'{vehicle_id}',
                                                                dates=datas_daily_activities,
                                                                hour1=selected_hours[0],
                                                                hour2=selected_hours[1])

    filtered_addresses = ConvertVehicleManagement(validation=True).convert_get_rout_history(get_history_activies)


    if len(filtered_addresses) > 0:
        map_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                    margin=dict(l=0, r=0, t=0, b=0), size=10,
                                    title="Posições do veiculo",
                                    x='Lat', y='Long').create_map_box(hover_name='Endereco', zoom=3,
                                                                      mapbox_style='open-street-map',
                                                                      hover_data=['Endereco',
                                                                                  'Motorista',
                                                                                  'Data Hora',
                                                                                  'Velocidade',
                                                                                  'Tipo de sinal'])

        table_positions = CreatGraphs(data_frame=filtered_addresses, height=600,
                                      margin=dict(l=0, r=15, t=0, b=0), size=10,
                                      title="Posições do veiculo",
                                      x='Lat', y='Long').create_table(
            columns=['Data Hora', 'Endereco', 'Motorista', 'Ignicao'])

        return map_positions, table_positions

    map_positions_black, table_positions_blanck = return_blancks()

    return map_positions_black, table_positions_blanck


@app.callback(
    Output('dropdown-select-all-LicencePlate', 'options'),
    Input('dropdown-select-all-vehicle-group', 'value')
)

def update_licence_plate_options(selected_group):
    if selected_group != 'Todos':
        filtered_vehicles_group_id = list(GetVehicleGroup[GetVehicleGroup['Name'] == selected_group]['Id'].unique())
        filtered_vehicles = GetVehicles[GetVehicles['GroupId'].isin(filtered_vehicles_group_id)]
        options = [{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
            {'label': placa, 'value': placa} for placa in
            filtered_vehicles['LicencePlate'].unique()]
        return options

    options = [{'label': 'Selecionar Tudo', 'value': 'Todos'}] + [
        {'label': placa, 'value': placa} for placa in
        GetVehicles['LicencePlate'].unique()]
    return options


@app.callback(
    Output("card-vehicles-activies", "children"),
    Output("card-drivers-authenticates", "children"),
    Output("card-vehicles-on", "children"),
    Output("activies-today-all-vehicle", "figure"),
    Output("positions-today-all-vehicle", "figure"),
    Input("dropdown-select-all-LicencePlate", "value"),
    Input("dropdown-enginie_status-all-vehicle", "value"),
    Input("dropdown-select-all-vehicle-group", "value"),
    Input('interval-component-map', 'n_intervals'),
)
def update_today_all_vehicles(selected_licence_plate, selected_engine_status, selected_group, n_intervals):
    def return_blancks():
        blanck_data = pd.DataFrame(
            {
                'Lat': [], 'Long': [], 'DateTime': [], 'Endereco': [],
                'Motorista': [], 'Ignicao': [], 'Placa': [], 'Velocidade': [],
            }
        )
        map_positions_black = CreatGraphs(data_frame=blanck_data, height=600,
                                          margin=dict(l=0, r=0, t=0, b=0), size=10,
                                          title="Posições do veiculo",
                                          x='Lat', y='Long').creat_map_box_blanck(zoom=3,
                                                                                  mapbox_style='open-street-map')

        table_positions_blanck = CreatGraphs(data_frame=blanck_data, height=600,
                                             margin=dict(l=0, r=15, t=0, b=0), size=10,
                                             title="Posições do veiculo",
                                             x='Lat', y='Long').create_table_blank(
        columns=['Ultima Menssagem', 'Endereco', 'Motorista', 'Ignicao', 'Placa'])

        vehicles_activies = "Sem dados"
        drivers_authenticates = "Sem dados"
        vehicles_on = "Sem dados"

        return (vehicles_activies, drivers_authenticates, vehicles_on,
                table_positions_blanck, map_positions_black)


    def not_blank(DataFrame = pd.DataFrame()):
        table_positions = CreatGraphs(data_frame=DataFrame, height=600,
                                      margin=dict(l=0, r=15, t=0, b=0), size=10,
                                      title="Posições do veiculo",
                                      x='Lat', y='Long').create_table(
            columns=['Ultima Menssagem', 'Endereco', 'Motorista', 'Ignicao', 'Placa'])

        map_positions = (CreatGraphs(data_frame=DataFrame, height=600,
                                     margin=dict(l=0, r=0, t=0, b=0), size=10,
                                     title="Posições do veiculo",
                                     x='Lat', y='Long').create_map_box
                         (hover_name='Endereco', zoom=3,
                          mapbox_style='open-street-map',
                          hover_data=['Endereco',
                                      'Motorista',
                                      'Ultima Menssagem', 'Ignicao', 'Placa', 'Velocidade', 'Modelo'], destacar_primeiro_ultimo=False))

        vehicles_activies = f"{len(DataFrame['Placa'].unique())}"
        drivers_authenticates = f"{len(DataFrame['Motorista'].dropna().unique())}"
        vehicles_on = f"{len(DataFrame[DataFrame['Ignicao']=='Ligado'])}"

        return vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions

    if 'Todos' not in selected_group and 'Todos' in selected_licence_plate:
        filtered_vehicles_group_id = list(GetVehicleGroup[
                                              GetVehicleGroup['Name'] == selected_group]['Id'].unique())
        filtered_vehicles = GetVehicles[GetVehicles['GroupId'].isin(filtered_vehicles_group_id)]


        if len(filtered_vehicles) == 0:
            (vehicles_activies, drivers_authenticates, vehicles_on,
             map_positions_black, table_positions_blanck) = return_blancks()

            return (vehicles_activies, drivers_authenticates, vehicles_on,
                    table_positions_blanck, map_positions_black)


        get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                               licenseplate=filtered_vehicles['LicencePlate'].unique(),
                                                               vehicleids=filtered_vehicles['VehicleId'].unique().astype(str))


        GetVehicleInfoAll = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)
        GetVehicleInfoAll = GetVehicleInfoAll[GetVehicleInfoAll['Ultima Menssagem'].str[:10] == datetime.now().strftime('%d/%m/%Y')]



        if len(GetVehicleInfoAll) == 0:
            (vehicles_activies, drivers_authenticates, vehicles_on,
             table_positions_blanck, map_positions_black) = return_blancks()

            return (vehicles_activies, drivers_authenticates, vehicles_on,
                    table_positions_blanck, map_positions_black)


        if selected_engine_status != 'Todos':
            GetVehicleInfoAll = GetVehicleInfoAll[GetVehicleInfoAll['Ignicao'] == selected_engine_status]

        vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions = not_blank(
            GetVehicleInfoAll)

        return vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions



    if len(selected_licence_plate)==0:
        (vehicles_activies, drivers_authenticates, vehicles_on,
         table_positions_blanck, map_positions_black) = return_blancks()

        return (vehicles_activies, drivers_authenticates, vehicles_on,
                table_positions_blanck, map_positions_black)



    if 'Todos' in selected_licence_plate:
        get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                               licenseplate=[''],
                                                               vehicleids=[''])
        GetVehicleInfoAll = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)
        GetVehicleInfoAll = GetVehicleInfoAll[GetVehicleInfoAll['Ultima Menssagem'].str[:10]==datetime.now().strftime('%d/%m/%Y')]


    elif len(selected_licence_plate) == 1:
        vehicle_id = GetVehicles[(GetVehicles['LicencePlate']==selected_licence_plate[0])]['VehicleId'].unique().astype(str)
        get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                               licenseplate=selected_licence_plate,
                                                               vehicleids=vehicle_id)
        GetVehicleInfoAll = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)
        GetVehicleInfoAll = GetVehicleInfoAll[
        GetVehicleInfoAll['Ultima Menssagem'].str[:10] == datetime.now().strftime('%d/%m/%Y')]


        if len(GetVehicleInfoAll) == 1:
            vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions = not_blank(GetVehicleInfoAll)
            return vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions

        else:
            (vehicles_activies, drivers_authenticates, vehicles_on,
             table_positions_blanck, map_positions_black) = return_blancks()
            return (vehicles_activies, drivers_authenticates, vehicles_on,
                table_positions_blanck, map_positions_black)

    else:
        vehicle_id = GetVehicles[(GetVehicles['LicencePlate'].isin(selected_licence_plate))]['VehicleId'].unique().astype(str)
        get_vehicle_info = vehicle_management.get_vehicle_info(second_rout=get_vehicles_info,
                                                               licenseplate=selected_licence_plate,
                                                               vehicleids=vehicle_id)
        GetVehicleInfoAll = ConvertVehicleManagement(validation=True).convert_get_vehicles_info(get_vehicle_info)
        GetVehicleInfoAll = GetVehicleInfoAll[
        GetVehicleInfoAll['Ultima Menssagem'].str[:10] == datetime.now().strftime('%d/%m/%Y')]


    if selected_engine_status and selected_engine_status != 'Todos':
        GetVehicleInfoAll = GetVehicleInfoAll[GetVehicleInfoAll['Ignicao']==selected_engine_status]

    vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions = not_blank(GetVehicleInfoAll)
    return vehicles_activies, drivers_authenticates, vehicles_on, table_positions, map_positions



##callback de atualização das bases de dados da pointer
##Bases de veiculos, de motoristas, carteira de veiculos, e calendario
@app.callback(
    Output('dummy-output', 'children'),
    Input('interval-component-update-databases', 'n_intervals')
)
def update_data_bases(n_intervals):
    global GetVehicles, GetVehicleGroup, GetDrivers, calendario, vehicle_management

    login = ApiPointer(url=url_base, user_name=params['login'], password=params['senha'])
    token = login.login(login_rout)
    account_administration = AccountAdministration(url=url_base, rout=account_administration_rout,
                                                   token_for_access=token, verify=False)
    getvehiclesgroups = account_administration.get_accounts(second_rout=get_vehicle_groups)
    GetVehicleGroup = ConvertAccountAdministration(validation=True).convert_get_vehicle_groups(getvehiclesgroups)
    vehicle_management = VehicleManagement(url=url_base,
                                           rout=vehicle_management_rout, token_for_access=token, verify=False)
    getvehicles = vehicle_management.get_vehicles(get_vehicles)
    GetVehicles = ConvertVehicleManagement(validation=True).convert_get_vehicles(getvehicles)
    driver_management = DriverManagement(url=url_base, rout=driver_rout, token_for_access=token, verify=False)
    drivers = driver_management.get_drivers(second_rout=get_drivers)
    GetDrivers = ConvertDriverManagement(validation=True).convert_get_drivers(drivers)

    return f"V0.1 Beta (teste) Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

if __name__=="__main__":
    app.run_server(host="0.0.0.0", debug=False)
