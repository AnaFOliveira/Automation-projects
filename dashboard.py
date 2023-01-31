import dash
from dash import Input, Output
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import numpy as np


def to_text(list_of_strings: list[str], split_separator: str = " ") -> str:
    """
    Creates text with all descriptions from the dataset.

    :param list_of_strings: list of strings to unify
    :param split_separator: separates the strings, default is a whitespace
    :return str: string with all descriptions
    """

    text = ""

    for string in list_of_strings:
        split = string.split(split_separator)
        description = ""
        for word in split:
            description += word + " "
        text += description

    return text


def tag_frequency(text):
    """
    Function adapted from the code of Prashant Saikia,
    https://github.com/PrashantSaikia/Wordcloud-in-Plotly/blob/master/plotly_wordcloud.py
    """
    wc = WordCloud(stopwords=set(STOPWORDS), max_words=200)
    wc.generate(text)

    word_list = []
    freq_list = []

    for (word, freq), _, _, _, _ in wc.layout_:
        if freq < 0.15:
            pass
        else:
            word_list.append(word)
            freq_list.append(freq)

    # get the relative occurrence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(round(i * 100, 0))

    trace = {
        "type": "bar",
        "x": new_freq_list,
        "y": word_list,
        "marker": {"color": "rgb(222, 113, 88)"},
        "orientation": "h",
    }

    layout = go.Layout(
        {
            "xaxis": {
                "title": "Relative Frequency",
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
            },
            "yaxis": {"title": "Tags", "gridcolor": "white", "zeroline": False},
            "title": "Series Description most used tags",
        }
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def slice_freq(db):
    fig = px.histogram(db, x="SliceThickness")
    fig.update_layout(
        {
            "xaxis": {"title": "Slice Thickness", "zeroline": False},
            "yaxis": {"title": "Frequency", "gridcolor": "white", "zeroline": False},
            "title": "Slice Thickness frequency",
        }
    )
    return fig


def hours_plot_original(df):
    """Creates plot with hourly distribution of this specific dataset days"""
    import plotly.figure_factory as ff

    df["Hour"] = df["LastUpdate"].dt.hour
    df["Day"] = df["LastUpdate"].dt.day
    day_20 = df.query("Day == 20")
    day_22 = df.query("Day == 22")
    day_25 = df.query("Day == 25")
    columns = [day_20["Hour"], day_22["Hour"], day_25["Hour"]]
    group_labels = ["Day 20", "Day 22", "Day 25"]
    trace = ff.create_distplot(columns, group_labels, bin_size=0.25)
    new_fig = go.Figure(trace)
    new_fig.update_layout(
        title="Most common hours of Strokes (or of the registration)",
        xaxis={"title": "Hours"},
        yaxis={"title": "Frequency"},
        hovermode="closest",
    )
    return new_fig


def hours_plot(df, day):
    """Creates plot with hourly distribution of this specific dataset days"""

    df["Hour"] = df["LastUpdate"].dt.hour
    df["Day"] = df["LastUpdate"].dt.day

    weekday_dict = {
        "Mon": 0,
        "Tue": 1,
        "Wed": 2,
        "Thur": 3,
        "Fri": 4,
        "Sat": 5,
        "Sun": 6,
    }

    df["Weekday"] = df["LastUpdate"].dt.dayofweek
    mask = df["Weekday"] == weekday_dict[day]

    unique, counts = np.unique(df[mask]["Hour"], return_counts=True)
    new_fig = go.Figure([go.Bar(x=unique, y=counts)])

    new_fig.update_layout(
        title="Most common hours of Strokes (or of the registration)",
        xaxis={"title": "Hours"},
        yaxis={"title": "Number of entries"},
        hovermode="closest",
    )

    return new_fig


def initialize_app(db):
    """Defines plots, aspect and logic of app"""

    column = db["SeriesDescription"].astype('str')
    descriptions = to_text(column,"__")
    tag_bar = tag_frequency(descriptions)
    slice_fig = slice_freq(db)

    # initiating the app
    app = dash.Dash()

    # defining the layout
    app.layout = html.Div(
        children=[
            html.H1(children="Methinks"),
            html.H3(
                children="Methinks vision is to provide universal and timely medical assistance to enable life-saving "
                "treatments worldwide. Our first focus is on stroke, the second most common cause of death "
                "and a major cause of disability globally."
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id="word_frequency",
                                figure=tag_bar,
                            ),
                        ],
                        style={"width": "50%", "display": "inline-block"},
                    ),
                    html.Div(
                        [dcc.Graph(id="slice_thickness", figure=slice_fig)],
                        style={"width": "50%", "display": "inline-block"},
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="dropdown",
                        options=["Wed", "Fri", "Mon"],
                        value="Fri",
                        clearable=False,
                    ),
                    dcc.Graph(id="dates"),
                ],
                style={"width": "100%", "display": "inline-block"},
            ),
        ]
    )

    @app.callback(Output("dates", "figure"), Input("dropdown", "value"))
    def update_bar_chart(day):
        figure = hours_plot(db, day)
        return figure

    return app


# running the app
if __name__ == "__main__":
    data_base = pd.read_csv("csv/series.csv", parse_dates=["LastUpdate"])
    dash_app = initialize_app(data_base)
    dash_app.run_server()
