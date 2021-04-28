import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker



import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#------------------------------------------------------------------------------

# Import Data

# engine = create_engine('sqlite:///sfapts.db', pool_pre_ping = True)
# with engine.connect() as connection:
#     dbdata = connection.execute(text("SELECT * FROM apartment"))
#     df = pd.DataFrame(dbdata)

df = pd.read_csv("sfaptsscraper/sfaptsscraper/sfapts.csv")
df['neighborhood'] = df['neighborhood'].fillna('San Francisco')

# Aggregated Price Data

dff = df.groupby('neighborhood').agg(
        {'price': [
            'count',
            'mean',
            'std',
            'min',
            'max'
        ]}
    ).sort_values(
        by=('price','count'), ascending = False
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
        value = dff.neighborhood[:3]
    ),

    html.H2('Price Histogram for Selected Neighborhoods'),

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


if __name__ == '__main__':
    app.run_server(debug=True)