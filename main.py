from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from data import countries_df, totals_df, dropdown_options
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    title="Confirmed By Country",
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    size_max=40,
    size="Confirmed",
    hover_name="Country_Region",
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    hover_data={"Confirmed": ":,", "Deaths": ":,", "Country_Region": False},
    labels={"conditions": "Condition", "count": "Count"},
)

bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={
        "count": ":,",
        "condition": False,
    },
    labels={"condition": "Condition", "count": "Count", "color": "Conditions"},
)

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 50})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(6, 1fr)",
                "gap": 50,
            },
            children=[
                html.Div(
                    style={"grid-column": "span 4"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(
                    style={"grid-column": "span 2"},
                    children=[make_table(countries_df)],
                ),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(6, 1fr)",
                "gap": 50,
            },
            children=[
                html.Div(
                    style={"grid-column": "span 2"},
                    children=[dcc.Graph(figure=bars_graph)],
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        html.H2(children=["country"], id="country-output"),
                    ]
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("country-output", "children"), [Input("country", "value")]
)
def update_hello(value):
    print(value)


if __name__ == "__main__":
    app.run_server(debug=True)
