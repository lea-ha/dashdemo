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
    ),
    html.Div(id='description-output')
    ]),
    html.Div([
        html.H1('Global Statistics'),
         dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Frequency of Movies Released Each Year', 'value': 'movies'},
            {'label': 'Frequency of Votes Each Year', 'value': 'votes'}
        ],
        value='movies'
    ),
    html.Div(id='output-graph'),
    html.Div(id='frequency-output'),
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

@callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph(selected_value):
    if selected_value == 'movies':
        data = df['Year of Release'].value_counts()
        title = 'Frequency of Movies Released Each Year'
        y_title = 'Number of Movies Released'
    elif selected_value == 'votes':
        data = df.groupby('Year of Release')['Votes'].sum()
        title = 'Frequency of Votes Each Year'
        y_title = 'Total Votes'
    
    return dcc.Graph(
        id='movies_years',
        figure={
            'data': [
                {'x': df['Year of Release'], 'y': data, 'type': 'bar'}
            ],
            'layout': {
                'title': title,
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': y_title}
            }
        }
    )


@callback(
    Output('description-output', 'children'),
    [Input('graph-with-slider', 'hoverData')]
)
def display_description(hoverData):

    if hoverData is not None:
        hovertext = hoverData['points'][0]['hovertext']
        description = df.loc[df['Movie Name'] == hovertext, 'Description'].iloc[0]
        return hovertext,":", description
    else:
        return ""
   

if __name__ == '__main__':
    app.run(debug=True)



