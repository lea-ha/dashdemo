from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px


df = pd.read_csv('Top Ranked Real Movies Dataset.csv', index_col='Unnamed: 0')
df = df.dropna()
df['Year of Release'] = pd.to_numeric(df['Year of Release'], errors='coerce')
df = df[df['Year of Release'] < 0]
df['Year of Release'] = df['Year of Release']*-1
df = df[~df['Gross'].str.startswith('#')]
df['Gross'] = df['Gross'].str.replace('M', '0').str.replace('$', '').astype(float)

#votes numeric
df['Votes'] = df['Votes'].str.replace(',', '')
df['Votes'] = pd.to_numeric(df['Votes'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://cdn.jsdelivr.net/npm/water.css@2/out/water.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout= html.Div([
    html.H1('Movies Statistics over the years'),
    html.Div([
       dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['Year of Release'].min(),
            df['Year of Release'].max(),
            step=5,
            value=df['Year of Release'].min(),
            marks={str(year): str(year) for year in range(1930, 2024, 5)},
            id='year-slider'
    )
    ])
])
@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):

    years_to_filter = range(selected_year - 5, selected_year + 1)
    filtered_df = df[df['Year of Release'].isin(years_to_filter)]

    y_ticks = np.arange(df['Gross'].min(), df['Gross'].max(), 100)
    y_ticktext = [f"${int(gross)}M" for gross in y_ticks]

    fig = px.scatter(filtered_df, x="Votes", y="Gross",
                     size="Votes", hover_name="Movie Name",
                     size_max=55).update_yaxes(tickvals=y_ticks, ticktext=y_ticktext)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run(debug=True)



