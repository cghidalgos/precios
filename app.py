from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# Funciones para las Estrategias de Precios
def skimming_pricing(price_initial, price_decrement, sales_initial, time_periods):
    prices = [price_initial - price_decrement * t for t in range(time_periods)]
    sales = [sales_initial - 10 * t for t in range(time_periods)]  # Asumimos que las ventas disminuyen
    revenue = [p * s for p, s in zip(prices, sales)]
    return revenue

def penetration_pricing(price_initial, sales_initial, growth_rate, time_periods):
    prices = [price_initial for _ in range(time_periods)]
    sales = [sales_initial * (1 + growth_rate)**t for t in range(time_periods)]
    revenue = [p * s for p, s in zip(prices, sales)]
    return revenue

def cost_plus_pricing(cost, margin, sales_initial, time_periods):
    price = cost * (1 + margin)
    sales = [sales_initial for _ in range(time_periods)]
    revenue = [price * s for s in sales]
    return revenue

# Crear la aplicación Flask
server = Flask(__name__)

# Crear la aplicación Dash
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de Dash
app.layout = dbc.Container([
    html.H1("Estrategias de Precios", className="text-center my-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Precio Inicial (Skimming y Penetración):"),
            html.P("Este es el precio inicial del producto que se utilizará en las estrategias de precios de skimming y penetración."),
            dcc.Input(id='price_initial', value=100, type='number', className="form-control"),
        ], md=4),
        
        dbc.Col([
            html.Label("Decremento de Precio (Skimming):"),
            html.P("Este es el monto por el cual se reducirá el precio en cada período en la estrategia de precios de skimming."),
            dcc.Input(id='price_decrement', value=5, type='number', className="form-control"),
        ], md=4),
        
        dbc.Col([
            html.Label("Crecimiento de Ventas (Penetración):"),
            html.P("Este es el crecimiento porcentual de las ventas en cada período en la estrategia de precios de penetración."),
            dcc.Input(id='growth_rate', value=0.1, type='number', className="form-control"),
        ], md=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Costo (Costo más Margen):"),
            html.P("Este es el costo de producción del producto, utilizado en la estrategia de precios de costo más margen."),
            dcc.Input(id='cost', value=30, type='number', className="form-control"),
        ], md=6),
        
        dbc.Col([
            html.Label("Margen (Costo más Margen):"),
            html.P("Este es el margen de beneficio sobre el costo de producción del producto en la estrategia de precios de costo más margen."),
            dcc.Input(id='margin', value=0.5, type='number', className="form-control"),
        ], md=6)
    ], className="mt-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='revenue-graph', className="mt-4")
        ])
    ]),
    
    html.H2("Descripción de la Gráfica", className="mt-4"),
    html.P("La gráfica compara los ingresos generados por diferentes estrategias de precios a lo largo de varios períodos. "
           "Cada línea representa una estrategia de precios diferente y muestra cómo varían los ingresos con el tiempo.")
])

# Callback para actualizar el gráfico
@app.callback(
    Output('revenue-graph', 'figure'),
    [
        Input('price_initial', 'value'),
        Input('price_decrement', 'value'),
        Input('growth_rate', 'value'),
        Input('cost', 'value'),
        Input('margin', 'value')
    ]
)
def update_graph(price_initial, price_decrement, growth_rate, cost, margin):
    time_periods = 10
    sales_initial = 1000
    
    revenue_skimming = skimming_pricing(price_initial, price_decrement, sales_initial, time_periods)
    revenue_penetration = penetration_pricing(price_initial, sales_initial, growth_rate, time_periods)
    revenue_cost_plus = cost_plus_pricing(cost, margin, sales_initial, time_periods)
    
    figure = {
        'data': [
            go.Scatter(x=list(range(time_periods)), y=revenue_skimming, mode='lines', name='Skimming Pricing'),
            go.Scatter(x=list(range(time_periods)), y=revenue_penetration, mode='lines', name='Penetration Pricing'),
            go.Scatter(x=list(range(time_periods)), y=revenue_cost_plus, mode='lines', name='Cost Plus Pricing')
        ],
        'layout': go.Layout(
            title='Comparación de Ingresos por Estrategias de Precios',
            xaxis={'title': 'Períodos de Tiempo'},
            yaxis={'title': 'Ingresos'}
        )
    }
    
    return figure

# Ruta principal de Flask
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)  # Cambia el puerto aquí si es necesario
    server.run(debug=True, port=5000)  # Asegúrate de que este puerto no esté en uso
