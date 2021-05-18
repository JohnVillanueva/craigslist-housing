import os
# from pymongo import MongoClient
from sqlalchemy import create_engine, text, select

import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


MAPBOX_TOKEN = os.environ['MAPBOX_TOKEN']

app = dash.Dash(__name__)

server = app.server

#------------------------------------------------------------------------------
# Import Data

# # Path Finder Function: https://stackoverflow.com/questions/1724693/find-a-file-in-python
# def find(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return os.path.join(root, name)
# CONNECTION_STRING = 'sqlite:///' + find('sfapts.db', os.getcwd() + '/..') #added parent directory to path; app file is in different directory branch than database

CONNECTION_STRING = os.environ['CONNECTION_STRING']
engine = create_engine(CONNECTION_STRING)
with engine.connect() as connection:
    dbdata = connection.execute(text("SELECT * FROM apartment"))
    df = pd.DataFrame(dbdata, columns = dbdata.keys())

# user = os.environ['DB_USERNAME']
# password = os.environ['DB_PASSWORD']
# host = os.environ['DB_HOST']
# db_name = os.environ['DB_NAME']
# CONNECTION_STRING = f'mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority'

# db = MongoClient(CONNECTION_STRING)['craigslist-scraperbase']
# df = pd.DataFrame(list(db.apartment.find()))

# Aggregated Price Data

dff = df.groupby('neighborhood').agg(
        {'price': [
            'count',
            'mean',
            'std'
        ]}
    ).sort_values(
        by=('price','count'),
        ascending = False
    )

dff.columns = dff.columns.droplevel()
dff = dff.reset_index()
#------------------------------------------------------------------------------
# APP Layout

app.layout = html.Div([

    html.H1('Craigslist Apartment Hunting Companion - San Francisco', style={'text-align': 'center'}),

    dcc.Checklist(
        id='neighborhood-options',
        options = [{'label': neighborhood, 'value': neighborhood} for neighborhood in df.neighborhood.unique()],
        value = dff.neighborhood[:10]
    ),

    html.H2('Geo Scatterplot of Selected Neighborhoods'),

    dcc.Graph(id='geoscatterplot-graph'),

    html.H2('Price Boxplots by Neighborhood'),

    dcc.Graph(id='neighborhood-boxplots'),

    html.H2('Aggregate Price Histogram for Selected Neighborhoods'),

    dcc.Graph(id='price-histogram'),

    html.H2('Pricing Statistics by Neighborhood'),

    dash_table.DataTable(
        id = 'price-summaries',
        columns = [{"name": i, "id": i} for i in dff.columns],
        sort_action = 'native',
        selected_columns = [],
        selected_rows = [],
        page_current = 0,
        page_size = 10,
    )

])

#------------------------------------------------------------------------------
# APP Callbacks

@app.callback(
    Output('price-histogram', 'figure'),
    Input('neighborhood-options', 'value')
)
def apts_by_neighborhood(neighborhood):
    filtered_df = df.loc[df.neighborhood.isin(neighborhood),]
    figure = px.histogram(filtered_df, x='price')
    return figure

@app.callback(
    Output('price-summaries', 'data'),
    Input('neighborhood-options', 'value')
)
def neighborhood_price_stats(neighborhood):
    filtered_dff = dff.loc[dff.neighborhood.isin(neighborhood),]
    return filtered_dff.to_dict('records')

@app.callback(
    Output('geoscatterplot-graph', 'figure'),
    Input('neighborhood-options', 'value')
)
def mapbox_scatter(neighborhood):
    filtered_df = df.loc[df.neighborhood.isin(neighborhood),]
    px.set_mapbox_access_token(MAPBOX_TOKEN)
    figure = px.scatter_mapbox(
        filtered_df, lat='latitude', lon='longitude', color = 'price', size = 'bedrooms', hover_name='name',
        color_continuous_scale = px.colors.diverging.Earth, size_max = 10, zoom=10)
    return figure

@app.callback(
    Output('neighborhood-boxplots', 'figure'),
    Input('neighborhood-options', 'value')
)
def neighborhood_boxplots(neighborhood):
    filtered_df = df.loc[df.neighborhood.isin(neighborhood),]
    figure = px.box(filtered_df, x='neighborhood', y='price', color='neighborhood')
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)

#------------------------------------------------------------------------------


