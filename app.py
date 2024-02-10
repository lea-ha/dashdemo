from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://cdn.jsdelivr.net/npm/water.css@2/out/water.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv('Top Ranked Real Movies Dataset.csv', index_col='Unnamed: 0')
df = df.dropna()
df['Year of Release'] = pd.to_numeric(df['Year of Release'], errors='coerce')
df = df[df['Year of Release'] < 0]
df['Year of Release'] = df['Year of Release']*-1

app.layout= html.Div([
    html.Div([
        html.H1(df.columns)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)



