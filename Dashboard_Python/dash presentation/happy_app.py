# -------------------------------------------------------------
# 1- WORLD HAPPINESS DASHBOARD: FINAL WEB APPLICATION
# -------------------------------------------------------------

import dash
from dash import html, dcc, dash_table, Input, Output, State
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


# -------------------------------------------------------------
# 2- LOAD THE CLEANED DATASET
# -------------------------------------------------------------


# Load the cleaned dataset.
happiness = pd.read_csv("happiness15-19.csv")

available_years = [
    int(year)
    for year in sorted(happiness["Year"].unique())
]

available_countries = sorted(
    happiness["Country"].unique()
)


# -------------------------------------------------------------
# 3- READABLE VARIABLE LABELS AND DICTIONARIES FOR DASHBOARD CONTROLS
# -------------------------------------------------------------

variable_labels = {
    "Rank": "Happiness Rank",
    "Happiness_Score": "Happiness Score",
    "GDP": "GDP per Capita",
    "Social_Support": "Social Support",
    "Life_Expectancy": "Healthy Life Expectancy",
    "Freedom": "Freedom",
    "Generosity": "Generosity",
    "Trust": "Trust"
}

# -------------------------------------------------------------
# RANKING-RACE OPTIONS
# -------------------------------------------------------------

race_metrics = {
    "Happiness_Score": "Happiness Score",
    "GDP": "GDP per Capita",
    "Social_Support": "Social Support",
    "Life_Expectancy": "Healthy Life Expectancy",
    "Freedom": "Freedom",
    "Generosity": "Generosity",
    "Trust": "Trust"
}

race_years = [
    int(year)
    for year in sorted(happiness["Year"].unique())
]
# -------------------------------------------------------------
# SCATTERPLOT OPTIONS
# -------------------------------------------------------------

plot_variables = {
    "Rank": "Happiness Rank",
    "Happiness_Score": "Happiness Score",
    "GDP": "GDP per Capita",
    "Social_Support": "Social Support",
    "Life_Expectancy": "Healthy Life Expectancy",
    "Freedom": "Freedom",
    "Generosity": "Generosity",
    "Trust": "Trust"
}
# -------------------------------------------------------------
# TABLE OPTIONS AND COLUMN DEFINITIONS
# -------------------------------------------------------------

numeric_filter_columns = [
    "Rank",
    "Happiness_Score",
    "GDP",
    "Social_Support",
    "Life_Expectancy",
    "Freedom",
    "Generosity",
    "Trust"
]

numeric_filter_labels = {
    "Rank": "Happiness Rank",
    "Happiness_Score": "Happiness Score",
    "GDP": "GDP per Capita",
    "Social_Support": "Social Support",
    "Life_Expectancy": "Healthy Life Expectancy",
    "Freedom": "Freedom",
    "Generosity": "Generosity",
    "Trust": "Trust"
}

table_columns = [
    {
        "name": "Country",
        "id": "Country",
        "type": "text"
    },
    {
        "name": "Year",
        "id": "Year",
        "type": "numeric"
    },
    {
        "name": "Rank",
        "id": "Rank",
        "type": "numeric"
    },
    {
        "name": "Happiness Score",
        "id": "Happiness_Score",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "GDP per Capita",
        "id": "GDP",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "Social Support",
        "id": "Social_Support",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "Life Expectancy",
        "id": "Life_Expectancy",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "Freedom",
        "id": "Freedom",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "Generosity",
        "id": "Generosity",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    },
    {
        "name": "Trust",
        "id": "Trust",
        "type": "numeric",
        "format": {"specifier": ".3f"}
    }
]
# -------------------------------------------------------------
# DISTRIBUTION-GRID OPTIONS
# -------------------------------------------------------------

distribution_variables = {
    "Happiness_Score": "Happiness Score",
    "GDP": "GDP per Capita",
    "Social_Support": "Social Support",
    "Life_Expectancy": "Healthy Life Expectancy",
    "Freedom": "Freedom",
    "Generosity": "Generosity",
    "Trust": "Trust"
}

distribution_years = [
    int(year)
    for year in sorted(happiness["Year"].unique())
]


# -------------------------------------------------------------
# FIXED AXIS RANGES FOR THE DISTRIBUTION GRID
# -------------------------------------------------------------

distribution_ranges = {}

for variable in distribution_variables:
    variable_min = float(happiness[variable].min())
    variable_max = float(happiness[variable].max())

    variable_span = variable_max - variable_min
    padding = variable_span * 0.08

    if padding == 0:
        padding = 0.1

    distribution_ranges[variable] = [
        variable_min - padding,
        variable_max + padding
    ]

# -------------------------------------------------------------
# 5- CREATE THE BASIC ANIMATED MAP
# -------------------------------------------------------------

# Sort observations chronologically.
map_data = happiness.sort_values(
    ["Year", "Country"]
).copy()

# Use one fixed color range across all years.
# This ensures that the same score always has the same color.
minimum_score = map_data["Happiness_Score"].min()
maximum_score = map_data["Happiness_Score"].max()

animated_map = px.choropleth(
    map_data,

    # Identify geographic areas using country names.
    locations="Country",
    locationmode="country names",

    # Color countries using their happiness scores.
    color="Happiness_Score",

    # Show the country name at the top of the hover label.
    hover_name="Country",

    # Select the additional information shown on hover.
    hover_data={
        "Year": False,
        "Rank": True,
        "Happiness_Score": ":.3f",
        "GDP": False,
        "Social_Support": False,
        "Life_Expectancy": False,
        "Freedom": False,
        "Generosity": False,
        "Trust": False
    },

    # Create one frame for each report year.
    animation_frame="Year",
    animation_group="Country",

    # Preserve the meaning of colors across all frames.
    range_color=(minimum_score, maximum_score),
    color_continuous_scale="RdYlGn",

    labels={
        "Happiness_Score": "Happiness Score",
        "Rank": "Rank"
    },

    projection="natural earth"
)

# -------------------------------------------------------------
# ADD A DIFFERENT TITLE TO EACH FRAME
# -------------------------------------------------------------

for frame in animated_map.frames:
    year = frame.name

    frame.layout.update(
        title={
            "text": f"World Happiness Scores: {year}",
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 28
            }
        }
    )


# Set the title displayed before the animation starts.
first_year = int(map_data["Year"].min())

animated_map.update_layout(
    title={
        "text": f"World Happiness Scores: {first_year}",
        "x": 0.5,
        "xanchor": "center",
        "font": {
            "size": 28
        }
    }
)

# -------------------------------------------------------------
# FORMAT LAND, OCEANS, LAKES, AND BORDERS
# -------------------------------------------------------------

animated_map.update_geos(
    # Display oceans with a blue background.
    showocean=True,
    oceancolor="LightBlue",

    # Display lakes using the same blue family.
    showlakes=True,
    lakecolor="LightBlue",

    # Give countries with no recorded data a light-gray color.
    showland=True,
    landcolor="LightGray",

    # Show national borders and coastlines.
    showcountries=True,
    countrycolor="white",
    countrywidth=0.6,

    showcoastlines=True,
    coastlinecolor="gray",

    # Remove the rectangular border around the world map.
    showframe=False,

    # Use the natural-earth projection.
    projection_type="natural earth"
)

# -------------------------------------------------------------
# FORMAT THE FIGURE'S PADDING AND MARGIN
# -------------------------------------------------------------

# Reduce the top padding above the Play/Pause buttons.
animated_map.layout.updatemenus[0].pad.t = 8

# Reduce the top padding above the year slider.
animated_map.layout.sliders[0].pad.t = 8

animated_map.update_layout(
    height=600,
    template="plotly_white",

    margin={
        "r": 0,
        "t": 70,
        "l": 0,
        "b": 0
    },

    coloraxis_colorbar={
        "title": {
            "text": "Happiness<br>Score"
        }
    }
)


# -------------------------------------------------------------
# CONTROL ANIMATION SPEED AND FORCE LAYOUT REDRAWING
# -------------------------------------------------------------

# Choropleth frames must redraw so that each frame's title
# and map colors are updated correctly.
for button in animated_map.layout.updatemenus[0].buttons:
    if button.label == "&#9654;" or button.label == "Play":
        button.args[1]["frame"]["duration"] = 1200
        button.args[1]["frame"]["redraw"] = True
        button.args[1]["transition"]["duration"] = 300
        button.args[1]["fromcurrent"] = True

# Ensure slider-selected frames also redraw their layouts.
for step in animated_map.layout.sliders[0].steps:
    step["args"][1]["frame"]["redraw"] = True

# -------------------------------------------------------------
# 6- CREATE ONE DASH APPLICATION
# -------------------------------------------------------------

app = dash.Dash(
    __name__,
    title="World Happiness Dashboard",
    suppress_callback_exceptions=True
)

# Required later if the application is deployed with Gunicorn.
server = app.server




# -------------------------------------------------------------
# 7- SHARED TAB STYLES
# -------------------------------------------------------------

main_tab_style = {
    "padding": "12px",
    "fontWeight": "bold",
    "backgroundColor": "#F2F3F4",
    "border": "1px solid #D5D8DC"
}

main_tab_selected_style = {
    "padding": "12px",
    "fontWeight": "bold",
    "backgroundColor": "coral",
    "color": "black",
    "borderTop": "4px solid red"
}

nested_tab_style = {
    "padding": "9px",
    "backgroundColor": "HoneyDew"
}

nested_tab_selected_style = {
    "padding": "9px",
    "fontWeight": "bold",
    "backgroundColor": "LimeGreen",
    "color": "black"
}

# -------------------------------------------------------------
# DISTRIBUTION GRAPH-CELL HELPER
# -------------------------------------------------------------

def create_graph_cell(graph_id):
    """
    Create one consistently styled cell for the 2-by-4 grid.
    """

    return html.Div(
        [
            dcc.Graph(
                id=graph_id,
                responsive=True,
                config={
                    "displaylogo": False,
                    "responsive": True,
                    "modeBarButtonsToRemove": [
                        "lasso2d",
                        "select2d"
                    ]
                },
                style={
                    "width": "100%",
                    "height": "100%"
                }
            )
        ],
        style={
            "backgroundColor": "#fffafa",
            "border": "1px solid #e1b9b9",
            "borderRadius": "8px",
            "overflow": "hidden",
            "minWidth": "0",
            "minHeight": "0",
            "height": "100%"
        }
    )

# -------------------------------------------------------------
# ALL REUSABLE COMPONENTS
# -------------------------------------------------------------
# -------------------------------------------------------------
# 8- REUSABLE RANKING-RACE COMPONENT
# -------------------------------------------------------------

ranking_component = html.Div(
    [
        html.P(
            "Select an indicator, the number of countries, and whether "
            "to display the highest or lowest values.",
            style={
                "textAlign": "center",
                "fontSize": "16px",
                "margin": "5px 0 15px 0"
            }
        ),

        # -----------------------------------------------------
        # RANKING CONTROLS
        # -----------------------------------------------------

        html.Div(
            [
                # Metric selection
                html.Div(
                    [
                        html.Label(
                            "Metric:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="race-metric",
                            options=[
                                {
                                    "label": label,
                                    "value": column
                                }
                                for column, label in race_metrics.items()
                            ],
                            value="Happiness_Score",
                            clearable=False
                        )
                    ],
                    style={
                        "width": "42%",
                        "display": "inline-block",
                        "verticalAlign": "top"
                    }
                ),

                # Number of countries
                html.Div(
                    [
                        html.Label(
                            "Number of countries:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="race-top-n",
                            options=[
                                {
                                    "label": "Top/Bottom 10",
                                    "value": 10
                                },
                                {
                                    "label": "Top/Bottom 15",
                                    "value": 15
                                },
                                {
                                    "label": "Top/Bottom 20",
                                    "value": 20
                                },
                                {
                                    "label": "Top/Bottom 25",
                                    "value": 25
                                }
                            ],
                            value=10,
                            clearable=False
                        )
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "paddingLeft": "3%"
                    }
                ),

                # Highest or lowest values
                html.Div(
                    [
                        html.Label(
                            "Order:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="race-order",
                            options=[
                                {
                                    "label": "Highest values",
                                    "value": "highest"
                                },
                                {
                                    "label": "Lowest values",
                                    "value": "lowest"
                                }
                            ],
                            value="highest",
                            clearable=False
                        )
                    ],
                    style={
                        "width": "27%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "paddingLeft": "3%"
                    }
                )
            ],
            style={
                "backgroundColor": "HoneyDew",
                "padding": "15px",
                "borderLeft": "6px solid LimeGreen",
                "borderRadius": "10px",
                "marginBottom": "10px",
                "boxSizing": "border-box"
            }
        ),

        # The callback will place the animated chart here.
        dcc.Graph(
            id="final-ranking-race",
            responsive=True,
            config={
                "displaylogo": False,
                "responsive": True
            },
            style={
                "width": "100%",
                "minHeight": "600px"
            }
        )
    ]
)

# -------------------------------------------------------------
# 9- REUSABLE SCATTERPLOT COMPONENT
# -------------------------------------------------------------

scatter_component = html.Div(
    [
        html.P(
            "Select variables, report years, and a regression option.",
            style={
                "textAlign": "center",
                "fontSize": "16px",
                "margin": "5px 0 15px 0"
            }
        ),

        # -----------------------------------------------------
        # SIDEBAR AND GRAPH
        # -----------------------------------------------------

        html.Div(
            [
                # -------------------------------------------------
                # LEFT SIDEBAR
                # -------------------------------------------------

                html.Div(
                    [
                        html.H3(
                            "Plot Controls",
                            style={
                                "textAlign": "center",
                                "marginTop": "0",
                                "marginBottom": "20px"
                            }
                        ),

                        # Horizontal-axis variable
                        html.Div(
                            [
                                html.Label(
                                    "Horizontal axis:",
                                    style={
                                        "fontWeight": "bold",
                                        "display": "block",
                                        "marginBottom": "5px"
                                    }
                                ),

                                dcc.Dropdown(
                                    id="scatter-x-variable",
                                    options=[
                                        {
                                            "label": label,
                                            "value": column
                                        }
                                        for column, label
                                        in plot_variables.items()
                                    ],
                                    value="GDP",
                                    clearable=False
                                )
                            ],
                            style={
                                "width": "100%",
                                "marginBottom": "18px"
                            }
                        ),

                        # Vertical-axis variable
                        html.Div(
                            [
                                html.Label(
                                    "Vertical axis:",
                                    style={
                                        "fontWeight": "bold",
                                        "display": "block",
                                        "marginBottom": "5px"
                                    }
                                ),

                                dcc.Dropdown(
                                    id="scatter-y-variable",
                                    options=[
                                        {
                                            "label": label,
                                            "value": column
                                        }
                                        for column, label
                                        in plot_variables.items()
                                    ],
                                    value="Happiness_Score",
                                    clearable=False
                                )
                            ],
                            style={
                                "width": "100%",
                                "marginBottom": "18px"
                            }
                        ),

                        # Report-year selection
                        html.Div(
                            [
                                html.Label(
                                    "Report years:",
                                    style={
                                        "fontWeight": "bold",
                                        "display": "block",
                                        "marginBottom": "5px"
                                    }
                                ),

                                dcc.Dropdown(
                                    id="scatter-year-filter",
                                    options=[
                                        {
                                            "label": str(year),
                                            "value": year
                                        }
                                        for year in available_years
                                    ],
                                    value=available_years,
                                    multi=True,
                                    placeholder="Select years"
                                )
                            ],
                            style={
                                "width": "100%",
                                "marginBottom": "18px"
                            }
                        ),

                        # Regression selection
                        html.Div(
                            [
                                html.Label(
                                    "Regression line:",
                                    style={
                                        "fontWeight": "bold",
                                        "display": "block",
                                        "marginBottom": "5px"
                                    }
                                ),

                                dcc.Dropdown(
                                    id="scatter-regression",
                                    options=[
                                        {
                                            "label": "No regression",
                                            "value": "none"
                                        },
                                        {
                                            "label": (
                                                "Separate line for each year"
                                            ),
                                            "value": "year"
                                        },
                                        {
                                            "label": (
                                                "One line for all selected data"
                                            ),
                                            "value": "overall"
                                        }
                                    ],
                                    value="year",
                                    clearable=False
                                )
                            ],
                            style={
                                "width": "100%",
                                "marginBottom": "18px"
                            }
                        ),

                        # Number of displayed observations
                        html.Div(
                            id="scatter-record-count",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "15px",
                                "padding": "10px",
                                "backgroundColor": "white",
                                "borderRadius": "6px",
                                "textAlign": "center"
                            }
                        )
                    ],
                    style={
                        "width": "24%",
                        "backgroundColor": "HoneyDew",
                        "padding": "18px",
                        "borderLeft": "6px solid LimeGreen",
                        "borderRadius": "10px",
                        "boxSizing": "border-box"
                    }
                ),

                # -------------------------------------------------
                # RIGHT GRAPH PANEL
                # -------------------------------------------------

                html.Div(
                    [
                        dcc.Graph(
                            id="relationship-scatter",
                            responsive=True,
                            config={
                                "displaylogo": False,
                                "responsive": True
                            },
                            style={
                                "height": "650px",
                                "width": "100%"
                            }
                        )
                    ],
                    style={
                        "width": "74%",
                        "marginLeft": "2%",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxSizing": "border-box",
                        "overflow": "hidden"
                    }
                )
            ],
            style={
                "display": "flex",
                "alignItems": "stretch",
                "width": "100%"
            }
        )
    ]
)

# -------------------------------------------------------------
# 10- REUSABLE DISTRIBUTION-GRID COMPONENT
# -------------------------------------------------------------

distribution_component = html.Div(
    [
        html.P(
            "Compare seven country-level distributions from 2015 to 2019.",
            style={
                "textAlign": "center",
                "fontSize": "15px",
                "margin": "3px 0 10px 0"
            }
        ),

        html.Div(
            [
                # First row
                create_graph_cell("dist-happiness"),
                create_graph_cell("dist-gdp"),
                create_graph_cell("dist-support"),
                create_graph_cell("dist-health"),

                # Second row
                create_graph_cell("dist-freedom"),
                create_graph_cell("dist-generosity"),
                create_graph_cell("dist-trust"),

                # Final grid cell: controls
                html.Div(
                    [
                        html.H3(
                            "Animation Controls",
                            style={
                                "textAlign": "center",
                                "margin": "0 0 12px 0"
                            }
                        ),

                        html.Div(
                            id="distribution-year-label",
                            children="Report Year: 2015",
                            style={
                                "fontSize": "20px",
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "color": "darkred",
                                "marginBottom": "12px"
                            }
                        ),

                        html.Button(
                            "▶ Play",
                            id="distribution-play-button",
                            n_clicks=0,
                            style={
                                "display": "block",
                                "width": "120px",
                                "margin": "0 auto 15px auto",
                                "padding": "8px",
                                "fontWeight": "bold",
                                "backgroundColor": "crimson",
                                "color": "white",
                                "border": "1px solid darkred",
                                "borderRadius": "6px",
                                "cursor": "pointer"
                            }
                        ),

                        html.Label(
                            "Report year:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Slider(
                            id="distribution-year-slider",
                            min=min(distribution_years),
                            max=max(distribution_years),
                            step=1,
                            value=min(distribution_years),
                            marks={
                                year: str(year)
                                for year in distribution_years
                            },
                            tooltip={
                                "placement": "bottom",
                                "always_visible": False
                            }
                        ),

                        html.Label(
                            "Display points:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginTop": "22px",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="distribution-points",
                            options=[
                                {
                                    "label": "Outliers only",
                                    "value": "outliers"
                                },
                                {
                                    "label": "All countries",
                                    "value": "all"
                                },
                                {
                                    "label": "Hide points",
                                    "value": "none"
                                }
                            ],
                            value="outliers",
                            clearable=False
                        ),

                        html.Div(
                            id="distribution-record-count",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "14px",
                                "textAlign": "center",
                                "marginTop": "18px",
                                "padding": "8px",
                                "backgroundColor": "white",
                                "borderRadius": "6px"
                            }
                        ),

                        dcc.Interval(
                            id="distribution-interval",
                            interval=1600,
                            n_intervals=0,
                            disabled=True
                        )
                    ],
                    style={
                        "backgroundColor": "#e1b9b9",
                        "padding": "16px",
                        "borderLeft": "6px solid darkred",
                        "borderRadius": "8px",
                        "boxSizing": "border-box",
                        "height": "100%",
                        "minHeight": "0",
                        "overflow": "hidden"
                    }
                )
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
                "gridTemplateRows": "repeat(2, 285px)",
                "gap": "8px",
                "width": "100%"
            }
        )
    ],
    style={
        "backgroundColor": "snow",
        "padding": "8px 12px",
        "boxSizing": "border-box",
        "fontFamily": "Arial, sans-serif",
        "overflowX": "hidden"
    }
)

# -------------------------------------------------------------
# 11- REUSABLE INTERACTIVE-TABLE COMPONENT
# -------------------------------------------------------------

table_component = html.Div(
    [
        html.P(
            "Use the dashboard controls and the filter row below the column "
            "headings to explore the country-year observations.",
            style={
                "textAlign": "center",
                "fontSize": "16px",
                "margin": "5px 0 15px 0"
            }
        ),

        # -----------------------------------------------------
        # EXTERNAL TABLE FILTERS
        # -----------------------------------------------------

        html.Div(
            [
                # Country selection
                html.Div(
                    [
                        html.Label(
                            "Countries:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="table-country-filter",
                            options=[
                                {
                                    "label": country,
                                    "value": country
                                }
                                for country in available_countries
                            ],
                            value=[],
                            multi=True,
                            placeholder="All countries"
                        )
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "verticalAlign": "top"
                    }
                ),

                # Year-range selection
                html.Div(
                    [
                        html.Label(
                            "Report-year range:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.RangeSlider(
                            id="table-year-filter",
                            min=min(available_years),
                            max=max(available_years),
                            value=[
                                min(available_years),
                                max(available_years)
                            ],
                            step=1,
                            marks={
                                year: str(year)
                                for year in available_years
                            },
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            }
                        )
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "paddingLeft": "4%"
                    }
                ),

                html.Div(
                    style={"height": "25px"}
                ),

                # Variable selection
                html.Div(
                    [
                        html.Label(
                            "Variable to filter by range:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.Dropdown(
                            id="table-variable-filter",
                            options=[
                                {
                                    "label": numeric_filter_labels[column],
                                    "value": column
                                }
                                for column in numeric_filter_columns
                            ],
                            value="Happiness_Score",
                            clearable=False
                        )
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "verticalAlign": "top"
                    }
                ),

                # Dynamic numeric-range filter
                html.Div(
                    [
                        html.Label(
                            id="table-range-label",
                            children="Happiness Score range:",
                            style={
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "5px"
                            }
                        ),

                        dcc.RangeSlider(
                            id="table-numeric-range",
                            min=round(
                                float(
                                    happiness["Happiness_Score"].min()
                                ),
                                2
                            ),
                            max=round(
                                float(
                                    happiness["Happiness_Score"].max()
                                ),
                                2
                            ),
                            value=[
                                round(
                                    float(
                                        happiness[
                                            "Happiness_Score"
                                        ].min()
                                    ),
                                    2
                                ),
                                round(
                                    float(
                                        happiness[
                                            "Happiness_Score"
                                        ].max()
                                    ),
                                    2
                                )
                            ],
                            step=0.01,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            }
                        )
                    ],
                    style={
                        "width": "64%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "paddingLeft": "6%"
                    }
                )
            ],
            style={
                "backgroundColor": "pink",
                "padding": "15px",
                "borderLeft": "6px solid deeppink",
                "borderRadius": "10px",
                "marginBottom": "15px",
                "boxSizing": "border-box"
            }
        ),

        # Record count
        html.Div(
            id="table-record-count",
            children=(
                f"Records matching the selected filters: "
                f"{len(happiness)}"
            ),
            style={
                "fontWeight": "bold",
                "fontSize": "16px",
                "marginBottom": "10px"
            }
        ),

        # -----------------------------------------------------
        # INTERACTIVE DATA TABLE
        # -----------------------------------------------------

        dash_table.DataTable(
            id="happiness-table",
            columns=table_columns,
            data=happiness.to_dict("records"),

            # Table sorting
            sort_action="native",
            sort_mode="multi",

            # Keep the built-in filter row
            filter_action="native",

            # Pagination
            page_action="native",
            page_size=15,

            # Export filtered/sorted data
            export_format="csv",
            export_headers="display",

            style_table={
                "width": "100%",
                "overflowX": "auto",
                "border": "1px solid #D5D8DC"
            },

            style_header={
                "backgroundColor": "deeppink",
                "color": "white",
                "fontWeight": "bold",
                "textAlign": "center"
            },

            style_cell={
                "textAlign": "center",
                "padding": "6px",
                "fontSize": "13px",
                "minWidth": "82px",
                "width": "82px",
                "maxWidth": "100px",
                "whiteSpace": "normal"
            },

            style_cell_conditional=[
                {
                    "if": {"column_id": "Country"},
                    "textAlign": "left",
                    "minWidth": "155px",
                    "width": "155px",
                    "maxWidth": "180px"
                },
                {
                    "if": {"column_id": "Year"},
                    "minWidth": "58px",
                    "width": "58px",
                    "maxWidth": "65px"
                },
                {
                    "if": {"column_id": "Rank"},
                    "minWidth": "55px",
                    "width": "55px",
                    "maxWidth": "65px"
                },
                {
                    "if": {"column_id": "Happiness_Score"},
                    "minWidth": "90px",
                    "width": "90px",
                    "maxWidth": "100px"
                },
                {
                    "if": {
                        "column_id": [
                            "GDP",
                            "Social_Support",
                            "Life_Expectancy",
                            "Freedom",
                            "Generosity",
                            "Trust"
                        ]
                    },
                    "minWidth": "82px",
                    "width": "82px",
                    "maxWidth": "95px"
                }
            ],

            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#FFF0F5"
                }
            ]
        )
    ]
)

# -------------------------------------------------------------
# 12- FINAL APPLICATION LAYOUT
# -------------------------------------------------------------

app.layout = html.Div(
    [
        # -----------------------------------------------------
        # WEBSITE HEADER
        # -----------------------------------------------------

        html.Div(
            [
                html.H1(
                    "World Happiness Reports: 2015–2019",
                    style={
                        "margin": "0",
                        "fontSize": "34px"
                    }
                ),

                html.P(
                    "An interactive exploration of national life "
                    "evaluations and their associated indicators.",
                    style={
                        "fontSize": "17px",
                        "margin": "8px 0 0 0"
                    }
                )
            ],
            style={
                "backgroundColor": "#17324D",
                "color": "white",
                "padding": "22px",
                "textAlign": "center",
                "borderRadius": "0 0 12px 12px"
            }
        ),

        # -----------------------------------------------------
        # TOP-LEVEL WEBSITE TABS
        # -----------------------------------------------------

        dcc.Tabs(
            id="main-tabs",
            value="home-tab",

            children=[
                # =================================================
                # MAIN TAB 1: HOME
                # =================================================

                dcc.Tab(
                    label="Home",
                    value="home-tab",
                    style=main_tab_style,
                    selected_style=main_tab_selected_style,

                    children=[
                        html.Div(
                            [
                                html.H2(
                                    "Understanding World Happiness"
                                ),

                                html.P(
                                    "The World Happiness Report does not "
                                    "simply measure laughter or momentary "
                                    "enjoyment. Its principal score represents "
                                    "how respondents evaluate their lives."
                                ),

                                html.P(
                                    "The accompanying economic, social, health, "
                                    "freedom, generosity, and trust indicators "
                                    "are derived country-level values. They "
                                    "should be interpreted comparatively rather "
                                    "than as literal dollars, years of age, or "
                                    "percentages."
                                ),

                                html.H3("Project Questions"),

                                html.Ul(
                                    [
                                        html.Li(
                                            "Which countries report the "
                                            "highest happiness scores?"
                                        ),
                                        html.Li(
                                            "How do rankings change from "
                                            "2015 to 2019?"
                                        ),
                                        html.Li(
                                            "Which indicators have stronger "
                                            "relationships with happiness?"
                                        ),
                                        html.Li(
                                            "Which countries depart from the "
                                            "general patterns?"
                                        )
                                    ]
                                ),

                                html.H3("Dataset"),

                                html.P(
                                    f"The cleaned dataset contains "
                                    f"{len(happiness):,} country-year "
                                    f"observations covering "
                                    f"{happiness['Country'].nunique()} "
                                    f"country or territory names."
                                )
                            ],
                            style={
                                "backgroundColor": "HoneyDew",
                                "padding": "25px",
                                "borderLeft": "6px solid LimeGreen",
                                "borderRadius": "10px",
                                "margin": "20px"
                            }
                        )
                    ]
                ),

                # =================================================
                # MAIN TAB 2: GLOBAL OVERVIEW
                # =================================================

                dcc.Tab(
                    label="Global Overview",
                    value="overview-tab",
                    style=main_tab_style,
                    selected_style=main_tab_selected_style,

                    children=[
                        # -----------------------------------------
                        # NESTED TABS
                        # -----------------------------------------

                        dcc.Tabs(
                            id="overview-nested-tabs",
                            value="map-subtab",

                            children=[
                                dcc.Tab(
                                    label="World Map",
                                    value="map-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            id="map-tab-content",
                                            children=[
                                                html.H2(
                                                    "Animated World Map",
                                                    style={
                                                        "textAlign": "center"
                                                    }
                                                ),

                                                html.P(
                                                    "Use the year slider or "
                                                    "animation controls to "
                                                    "compare happiness scores "
                                                    "across countries.",
                                                    style={
                                                        "textAlign": "center"
                                                    }
                                                ),

                                                dcc.Graph(
                                                    id="final-happiness-map",
                                                    figure=animated_map,
                                                    responsive=True,
                                                    config={
                                                        "displaylogo": False,
                                                        "responsive": True
                                                    },
                                                    style={
                                                        "width": "100%",
                                                        "height": "650px"
                                                    }
                                                )
                                            ],
                                            style={"padding": "15px"}
                                        )
                                    ]
                                ),

                                dcc.Tab(
                                    label="Ranking Race",
                                    value="ranking-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            id="ranking-tab-content",
                                            children=[
                                                html.H2(
                                                    "Animated Country Ranking",
                                                    style={
                                                        "textAlign": "center"
                                                    }
                                                ),

                                                # Ranking controls and graph
                                                ranking_component
                                            ],
                                            style={"padding": "15px"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                # =================================================
                # MAIN TAB 3: RELATIONSHIPS
                # =================================================

                dcc.Tab(
                    label="Relationships",
                    value="relationships-tab",
                    style=main_tab_style,
                    selected_style=main_tab_selected_style,

                    children=[
                        dcc.Tabs(
                            id="relationships-nested-tabs",
                            value="scatter-subtab",

                            children=[
                                dcc.Tab(
                                    label="Scatterplot Explorer",
                                    value="scatter-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            id="scatter-tab-content",
                                            children=[
                                                # Your scatterplot sidebar
                                                # and graph will go here.
                                                html.H2(
                                                    "Relationship Explorer",
                                                    style={
                                                        "textAlign": "center"
                                                    }
                                                ),

                                                scatter_component
                                            ],
                                            style={"padding": "15px"}
                                        )
                                    ]
                                ),

                                dcc.Tab(
                                    label="Distributions",
                                    value="distribution-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            [
                                                html.H2(
                                                    "Indicator Distributions",
                                                    style={
                                                        "textAlign": "center",
                                                        "margin": "8px 0"
                                                    }
                                                ),

                                                distribution_component
                                            ],
                                            style={
                                                "padding": "10px"
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                # =================================================
                # MAIN TAB 4: DATA EXPLORER
                # =================================================

                dcc.Tab(
                    label="Data Explorer",
                    value="data-tab",
                    style=main_tab_style,
                    selected_style=main_tab_selected_style,

                    children=[
                        dcc.Tabs(
                            id="data-nested-tabs",
                            value="table-subtab",

                            children=[
                                dcc.Tab(
                                    label="Interactive Table",
                                    value="table-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            id="table-tab-content",
                                            children=[
                                                html.H2(
                                                    "Filtered Country-Year Data",
                                                    style={
                                                        "textAlign": "center"
                                                    }
                                                ),

                                                # Table filters and DataTable
                                                # will be inserted here.
                                                table_component
                                            ],
                                            style={"padding": "15px"}
                                        )
                                    ]
                                ),

                                dcc.Tab(
                                    label="Variables and Method",
                                    value="method-subtab",
                                    style=nested_tab_style,
                                    selected_style=nested_tab_selected_style,

                                    children=[
                                        html.Div(
                                            [
                                                html.H2(
                                                    "Variables and Interpretation"
                                                ),

                                                html.P(
                                                    "The Happiness Score is a "
                                                    "national life-evaluation "
                                                    "measure. The accompanying "
                                                    "indicators are derived "
                                                    "country-level values used "
                                                    "to explain differences in "
                                                    "national life evaluations."
                                                ),

                                                html.Ul(
                                                    [
                                                        html.Li(
                                                            "Happiness Score: "
                                                            "life evaluation on "
                                                            "a 0–10 scale."
                                                        ),
                                                        html.Li(
                                                            "Rank: 1 represents "
                                                            "the highest-scoring "
                                                            "country in a year."
                                                        ),
                                                        html.Li(
                                                            "GDP, support, health, "
                                                            "freedom, generosity, "
                                                            "and trust values are "
                                                            "comparative derived "
                                                            "indicators."
                                                        ),
                                                        html.Li(
                                                            "Associations and "
                                                            "regressions do not "
                                                            "prove causation."
                                                        )
                                                    ]
                                                )
                                            ],
                                            style={
                                                "backgroundColor": "HoneyDew",
                                                "padding": "25px",
                                                "borderLeft": (
                                                    "6px solid LimeGreen"
                                                ),
                                                "borderRadius": "10px",
                                                "margin": "20px"
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # -----------------------------------------------------
        # WEBSITE FOOTER
        # -----------------------------------------------------

        html.Div(
            [
                html.P(
                    " Maliheh Mahdavi Sefat - University of Minho - 2026 ",
                    "Python, Dash and Plotly Project",
                    style={"margin": "0"}
                )
            ],
            style={
                "backgroundColor": "#17324D",
                "color": "white",
                "textAlign": "center",
                "padding": "12px",
                "marginTop": "20px"
            }
        )
    ],
    style={
        "backgroundColor": "snow",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif"
    }
)

# -------------------------------------------------------------
# 13- HELPER: CREATE ONE DISTRIBUTION BOXPLOT
# -------------------------------------------------------------

def create_distribution_figure(
    filtered_data,
    variable,
    variable_label,
    point_setting
):
    """
    Create one compact boxplot with a fixed vertical range.
    """

    figure = px.box(
        filtered_data,
        y=variable,
        points=point_setting,
        hover_name="Country",
        hover_data={
            "Year": True,
            "Rank": True,
            "Happiness_Score": ":.3f",
            variable: ":.3f"
        },
        labels={
            variable: variable_label
        },
        color_discrete_sequence=["olive"]
    )

    if point_setting == "all":
        figure.update_traces(
            jitter=0.25,
            pointpos=0,
            marker={
                "size": 3,
                "opacity": 0.40
            }
        )

    figure.update_layout(
        title={
            "text": variable_label,
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 14
            }
        },

        template="plotly_white",

        yaxis={
            "range": distribution_ranges[variable],
            "title": "",
            "tickfont": {
                "size": 9
            },
            "gridcolor": "#E5E7E9",
            "zeroline": False
        },

        xaxis={
            "visible": False
        },

        showlegend=False,

        margin={
            "l": 42,
            "r": 12,
            "t": 38,
            "b": 12
        }
    )

    return figure

# -------------------------------------------------------------
# 14- CALLBACK: UPDATE THE RELATIONSHIP SCATTERPLOT
# -------------------------------------------------------------

@app.callback(
    Output("relationship-scatter", "figure"),
    Output("scatter-record-count", "children"),
    Input("scatter-x-variable", "value"),
    Input("scatter-y-variable", "value"),
    Input("scatter-year-filter", "value"),
    Input("scatter-regression", "value")
)
def update_relationship_plot(
    x_variable,
    y_variable,
    selected_years,
    regression_option
):
    """
    Filter the data by report year and create the selected
    scatterplot and regression lines.
    """

    # Start with a copy of the complete cleaned dataset.
    filtered_data = happiness.copy()

    # If all years are removed from the dropdown, use all years.
    if not selected_years:
        selected_years = available_years

    # Keep observations from the selected years.
    filtered_data = filtered_data[
        filtered_data["Year"].isin(selected_years)
    ].copy()

    # Treat Year as a categorical variable so that Plotly assigns
    # a separate color to each report year.
    filtered_data["Year_Label"] = (
        filtered_data["Year"].astype(str)
    )

    # Retrieve readable variable names for titles and axes.
    x_label = plot_variables[x_variable]
    y_label = plot_variables[y_variable]

    # ---------------------------------------------------------
    # HANDLE AN EMPTY RESULT
    # ---------------------------------------------------------

    if filtered_data.empty:
        empty_figure = go.Figure()

        empty_figure.add_annotation(
            text="No observations match the selected years.",
            x=0.5,
            y=0.5,
            showarrow=False,
            font={"size": 18}
        )

        empty_figure.update_layout(
            template="plotly_white",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )

        return empty_figure, "Observations displayed: 0"

    # ---------------------------------------------------------
    # CREATE THE GRAPH TITLE
    # ---------------------------------------------------------

    if x_variable == y_variable:
        title = f"{x_label} Plotted Against Itself"
    else:
        title = f"{y_label} in Relation to {x_label}"

    # These fields appear when the user hovers over a point.
    hover_fields = {
        "Year_Label": False,
        "Year": True,
        "Rank": True,
        "Happiness_Score": ":.3f",
        "GDP": ":.3f",
        "Social_Support": ":.3f",
        "Life_Expectancy": ":.3f",
        "Freedom": ":.3f",
        "Generosity": ":.3f",
        "Trust": ":.3f"
    }

    # ---------------------------------------------------------
    # OPTION 1: NO REGRESSION
    # ---------------------------------------------------------

    if regression_option == "none":
        figure = px.scatter(
            filtered_data,
            x=x_variable,
            y=y_variable,
            color="Year_Label",
            hover_name="Country",
            hover_data=hover_fields,
            opacity=0.75,
            title=title,
            labels={
                x_variable: x_label,
                y_variable: y_label,
                "Year_Label": "Year"
            }
        )

    # ---------------------------------------------------------
    # OPTION 2: ONE REGRESSION FOR EACH YEAR
    # ---------------------------------------------------------

    elif regression_option == "year":
        figure = px.scatter(
            filtered_data,
            x=x_variable,
            y=y_variable,
            color="Year_Label",
            trendline="ols",
            hover_name="Country",
            hover_data=hover_fields,
            opacity=0.70,
            title=f"{title}: Separate Annual Regressions",
            labels={
                x_variable: x_label,
                y_variable: y_label,
                "Year_Label": "Year"
            }
        )

    # ---------------------------------------------------------
    # OPTION 3: ONE OVERALL REGRESSION
    # ---------------------------------------------------------

    else:
        figure = px.scatter(
            filtered_data,
            x=x_variable,
            y=y_variable,
            color="Year_Label",
            trendline="ols",
            trendline_scope="overall",
            trendline_color_override="black",
            hover_name="Country",
            hover_data=hover_fields,
            opacity=0.70,
            title=f"{title}: Overall Regression",
            labels={
                x_variable: x_label,
                y_variable: y_label,
                "Year_Label": "Year"
            }
        )

    # ---------------------------------------------------------
    # FORMAT THE GRAPH
    # ---------------------------------------------------------

    # Apply this formatting only to point traces.
    # Regression-line traces remain unchanged.
    figure.update_traces(
        marker={
            "size": 8,
            "line": {
                "width": 0.5,
                "color": "white"
            }
        },
        selector={"mode": "markers"}
    )

    figure.update_layout(
        template="plotly_white",

        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 23}
        },

        legend_title_text="Report Year",

        margin={
            "l": 55,
            "r": 20,
            "t": 80,
            "b": 55
        }
    )

    return (
        figure,
        f"Observations displayed: {len(filtered_data)}"
    )

# -------------------------------------------------------------
# 15- CALLBACK: UPDATE THE ANIMATED COUNTRY RANKING
# -------------------------------------------------------------

@app.callback(
    Output("final-ranking-race", "figure"),
    Input("race-metric", "value"),
    Input("race-top-n", "value"),
    Input("race-order", "value")
)
def update_ranking_race(selected_metric, top_n, selected_order):
    """
    Create an animated horizontal ranking for the selected metric.
    """

    # Work with a copy of the complete cleaned dataset.
    race_data = happiness.copy()

    metric_label = race_metrics[selected_metric]

    # Use emoji-country labels if they were saved in the CSV.
    # Otherwise, use the ordinary country names.
    if "Country_Label" in race_data.columns:
        label_column = "Country_Label"
    else:
        label_column = "Country"

    # ---------------------------------------------------------
    # CALCULATE ANNUAL RANKS
    # ---------------------------------------------------------

    if selected_metric == "Happiness_Score":
        # Use the official annual happiness ranking.
        race_data["Metric_Rank"] = race_data["Rank"].astype(int)

    else:
        # Calculate a separate annual rank for the selected metric.
        # Rank 1 represents the highest value.
        race_data["Metric_Rank"] = (
            race_data.groupby("Year")[selected_metric]
            .rank(method="min", ascending=False)
            .astype(int)
        )

    # ---------------------------------------------------------
    # SELECT TOP OR BOTTOM COUNTRIES FOR EACH YEAR
    # ---------------------------------------------------------

    selected_year_frames = []

    for year in race_years:
        year_data = race_data[
            race_data["Year"] == year
        ].copy()

        if selected_order == "highest":
            year_selection = year_data.nlargest(
                top_n,
                selected_metric
            )

            # Horizontal bars are drawn from bottom to top.
            # Ascending order places the largest value at the top.
            year_selection = year_selection.sort_values(
                selected_metric,
                ascending=True
            )

        else:
            year_selection = year_data.nsmallest(
                top_n,
                selected_metric
            )

            # Descending order places the smallest value at the top.
            year_selection = year_selection.sort_values(
                selected_metric,
                ascending=False
            )

        selected_year_frames.append(year_selection)

    selected_data = pd.concat(
        selected_year_frames,
        ignore_index=True
    )

    # ---------------------------------------------------------
    # USE ACTUAL VALUES AS BAR LENGTHS
    # ---------------------------------------------------------

    # The same value will now always have the same bar length.
    selected_data["Display_Length"] = selected_data[selected_metric]

    selected_maximum = float(
        selected_data[selected_metric].max()
    )

    # Add room on the right for the value and rank labels.
    x_axis_minimum = 0
    x_axis_maximum = selected_maximum * 1.25

    if x_axis_maximum == 0:
        x_axis_maximum = 1

    # ---------------------------------------------------------
    # FORMAT LABELS
    # ---------------------------------------------------------

    selected_data["Actual_Value_Label"] = (
        selected_data[selected_metric]
        .map(lambda value: f"{value:.3f}")
    )

    selected_data["Rank_Label"] = (
        "#"
        + selected_data["Metric_Rank"].astype(str)
    )

    selected_data["Bar_Text"] = (
        selected_data["Actual_Value_Label"]
        + "   "
        + selected_data["Rank_Label"]
    )

    # ---------------------------------------------------------
    # CREATE ONE BAR TRACE
    # ---------------------------------------------------------

    def create_bar_trace(frame_data):
        """
        Create one annual horizontal-bar trace.
        """

        # Use NumPy arrays to avoid duplicate column-name errors
        # when the selected metric is Happiness_Score, GDP, etc.
        custom_hover_data = np.column_stack([
            frame_data["Country"],          # 0
            frame_data["Year"],             # 1
            frame_data["Metric_Rank"],      # 2
            frame_data[selected_metric],    # 3
            frame_data["Happiness_Score"],  # 4
            frame_data["Rank"],             # 5
            frame_data["GDP"],              # 6
            frame_data["Social_Support"],   # 7
            frame_data["Life_Expectancy"],  # 8
            frame_data["Freedom"],          # 9
            frame_data["Generosity"],       # 10
            frame_data["Trust"]             # 11
        ])

        return go.Bar(
            x=frame_data["Display_Length"],
            y=frame_data[label_column],

            orientation="h",
            width=0.55,

            text=frame_data["Bar_Text"],
            textposition="outside",
            cliponaxis=False,

            customdata=custom_hover_data,

            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Year: %{customdata[1]}<br>"
                f"{metric_label}: %{{customdata.3f}}<br>"
                "Metric rank: #%{customdata[2]}<br>"
                "Official happiness rank: #%{customdata[5]}<br>"
                "Happiness score: %{customdata.3f}<br>"
                "GDP: %{customdata.3f}<br>"
                "Social support: %{customdata.3f}<br>"
                "Healthy life expectancy: %{customdata.3f}<br>"
                "Freedom: %{customdata.3f}<br>"
                "Generosity: %{customdata.3f}<br>"
                "Trust: %{customdata.3f}"
                "<extra></extra>"
            ),

            marker={
                "color": "steelblue",
                "line": {
                    "color": "white",
                    "width": 0.6
                }
            }
        )

    # ---------------------------------------------------------
    # INITIAL FIGURE
    # ---------------------------------------------------------

    first_year = race_years[0]

    initial_data = selected_data[
        selected_data["Year"] == first_year
    ].copy()

    order_word = (
        "Highest"
        if selected_order == "highest"
        else "Lowest"
    )

    figure = go.Figure(
        data=[
            create_bar_trace(initial_data)
        ]
    )

    # ---------------------------------------------------------
    # ANIMATION FRAMES
    # ---------------------------------------------------------

    animation_frames = []

    for year in race_years:
        frame_data = selected_data[
            selected_data["Year"] == year
        ].copy()

        animation_frames.append(
            go.Frame(
                name=str(year),

                data=[
                    create_bar_trace(frame_data)
                ],

                layout=go.Layout(
                    title={
                        "text": (
                            f"{order_word} {top_n} Countries by "
                            f"{metric_label}: {year}"
                        ),
                        "x": 0.5,
                        "xanchor": "center"
                    }
                )
            )
        )

    figure.frames = animation_frames

    # ---------------------------------------------------------
    # YEAR-SLIDER STEPS
    # ---------------------------------------------------------

    slider_steps = []

    for year in race_years:
        slider_steps.append(
            {
                "label": str(year),
                "method": "animate",
                "args": [
                    [str(year)],
                    {
                        "frame": {
                            "duration": 700,
                            "redraw": True
                        },
                        "transition": {
                            "duration": 300
                        },
                        "mode": "immediate"
                    }
                ]
            }
        )

    # Increase chart height when more countries are selected.
    figure_height = {
        10: 650,
        15: 760,
        20: 880,
        25: 1000
    }[top_n]

    # ---------------------------------------------------------
    # FORMAT THE FIGURE
    # ---------------------------------------------------------

    figure.update_layout(
        title={
            "text": (
                f"{order_word} {top_n} Countries by "
                f"{metric_label}: {first_year}"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24}
        },

        height=figure_height,
        template="plotly_white",

        xaxis={
            # Fixed across every animation frame.
            "range": [x_axis_minimum, x_axis_maximum],
            "showticklabels": True,
            "tickformat": ".2f",
            "title": metric_label,
            "showgrid": True,
            "gridcolor": "#E5E7E9",
            "zeroline": True,
            "zerolinecolor": "#AAB7B8"
        },

        yaxis={
            "title": "",
            # Prevent country-name length from moving the plot.
            "automargin": False,
            "tickfont": {"size": 12},
            "ticksuffix": "  "
        },

        # Fixed margins preserve the chart position between years.
        margin={
            "l": 235,
            "r": 110,
            "t": 80,
            "b": 190,
            "pad": 0
        },

        showlegend=False,

        # Play and Pause buttons
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",

                "x": -0.03,
                "y": -0.18,
                "xanchor": "left",
                "yanchor": "top",

                "showactive": False,

                "buttons": [
                    {
                        "label": "▶ Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {
                                    "duration": 1100,
                                    "redraw": True
                                },
                                "transition": {
                                    "duration": 350
                                },
                                "fromcurrent": True,
                                "mode": "immediate"
                            }
                        ]
                    },
                    {
                        "label": "■ Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "transition": {
                                    "duration": 0
                                },
                                "mode": "immediate"
                            }
                        ]
                    }
                ]
            }
        ],

        # Year slider
        sliders=[
            {
                "active": 0,

                "x": 0.19,
                "y": -0.17,
                "len": 0.77,

                "xanchor": "left",
                "yanchor": "top",

                "pad": {
                    "t": 10,
                    "b": 0
                },

                "currentvalue": {
                    "prefix": "Year: ",
                    "font": {"size": 15}
                },

                "steps": slider_steps
            }
        ]
    )

    return figure

# -------------------------------------------------------------
# 16- CALLBACK: PLAY OR PAUSE DISTRIBUTION ANIMATION
# -------------------------------------------------------------

@app.callback(
    Output("distribution-interval", "disabled"),
    Output("distribution-play-button", "children"),
    Input("distribution-play-button", "n_clicks"),
    State("distribution-interval", "disabled")
)
def toggle_distribution_animation(n_clicks, currently_disabled):
    """
    Enable or disable automatic year advancement.
    """

    if not n_clicks:
        return True, "▶ Play"

    new_disabled_state = not currently_disabled

    if new_disabled_state:
        button_text = "▶ Play"
    else:
        button_text = "⏸ Pause"

    return new_disabled_state, button_text

# -------------------------------------------------------------
# 17- HELPER: CREATE ONE DISTRIBUTION BOXPLOT
# -------------------------------------------------------------

def create_distribution_figure(
    filtered_data,
    variable,
    variable_label,
    point_setting
):
    """
    Create one compact boxplot with a fixed vertical range.
    """

    figure = px.box(
        filtered_data,
        y=variable,
        points=point_setting,
        hover_name="Country",

        hover_data={
            "Year": True,
            "Rank": True,
            "Happiness_Score": ":.3f",
            variable: ":.3f"
        },

        labels={
            variable: variable_label
        },

        color_discrete_sequence=["olive"]
    )

    # Make individual country points smaller when all are visible.
    if point_setting == "all":
        figure.update_traces(
            jitter=0.25,
            pointpos=0,
            marker={
                "size": 3,
                "opacity": 0.40,
                "color": "darkred"
            }
        )

    figure.update_layout(
        title={
            "text": variable_label,
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 14
            }
        },

        template="plotly_white",

        # Keep the same scale for this variable in every year.
        yaxis={
            "range": distribution_ranges[variable],
            "title": "",
            "tickfont": {
                "size": 9
            },
            "gridcolor": "#E5E7E9",
            "zeroline": False
        },

        xaxis={
            "visible": False
        },

        showlegend=False,

        margin={
            "l": 42,
            "r": 12,
            "t": 38,
            "b": 12
        }
    )

    return figure
# -------------------------------------------------------------
# 18- CALLBACK: PLAY OR PAUSE DISTRIBUTION ANIMATION
# -------------------------------------------------------------

@app.callback(
    Output("distribution-interval", "disabled"),
    Output("distribution-play-button", "children"),
    Input("distribution-play-button", "n_clicks"),
    State("distribution-interval", "disabled")
)
def toggle_distribution_animation(n_clicks, currently_disabled):
    """
    Enable or disable automatic year advancement.
    """

    if not n_clicks:
        return True, "▶ Play"

    new_disabled_state = not currently_disabled

    if new_disabled_state:
        button_text = "▶ Play"
    else:
        button_text = "⏸ Pause"

    return new_disabled_state, button_text

# -------------------------------------------------------------
# 19- CALLBACK: ADVANCE DISTRIBUTION YEAR
# -------------------------------------------------------------

@app.callback(
    Output("distribution-year-slider", "value"),
    Input("distribution-interval", "n_intervals"),
    State("distribution-year-slider", "value"),
    prevent_initial_call=True
)
def advance_distribution_year(n_intervals, current_year):
    """
    Advance to the next year and restart after 2019.
    """

    current_index = distribution_years.index(int(current_year))

    next_index = (
        current_index + 1
    ) % len(distribution_years)

    return distribution_years[next_index]

# -------------------------------------------------------------
# 20- CALLBACK: UPDATE THE DISTRIBUTION GRID
# -------------------------------------------------------------

@app.callback(
    Output("dist-happiness", "figure"),
    Output("dist-gdp", "figure"),
    Output("dist-support", "figure"),
    Output("dist-health", "figure"),
    Output("dist-freedom", "figure"),
    Output("dist-generosity", "figure"),
    Output("dist-trust", "figure"),
    Output("distribution-year-label", "children"),
    Output("distribution-record-count", "children"),
    Input("distribution-year-slider", "value"),
    Input("distribution-points", "value")
)
def update_distribution_grid(selected_year, selected_points):
    """
    Create all seven distribution plots for the selected year.
    """

    filtered_data = happiness[
        happiness["Year"] == selected_year
    ].copy()

    if selected_points == "none":
        point_setting = False
    else:
        point_setting = selected_points

    figures = []

    for variable, variable_label in distribution_variables.items():
        figures.append(
            create_distribution_figure(
                filtered_data=filtered_data,
                variable=variable,
                variable_label=variable_label,
                point_setting=point_setting
            )
        )

    return (
        figures[0],
        figures[1],
        figures[2],
        figures[3],
        figures[4],
        figures[5],
        figures[6],
        f"Report Year: {selected_year}",
        f"Countries displayed: {len(filtered_data)}"
    )

# -------------------------------------------------------------
# 21- CALLBACK: DISPLAY THE SEVEN DISTRIBUTION PLOTS
# -------------------------------------------------------------

@app.callback(
    Output("dist-happiness", "figure"),
    Output("dist-gdp", "figure"),
    Output("dist-support", "figure"),
    Output("dist-health", "figure"),
    Output("dist-freedom", "figure"),
    Output("dist-generosity", "figure"),
    Output("dist-trust", "figure"),
    Output("distribution-year-label", "children"),
    Output("distribution-record-count", "children"),

    Input("distribution-year-slider", "value"),
    Input("distribution-points", "value")
)
def update_distribution_grid(selected_year, selected_points):
    """
    Create all seven boxplots for the selected report year.
    """

    # Keep only observations from the selected year.
    filtered_data = happiness[
        happiness["Year"] == selected_year
    ].copy()

    # Convert the dropdown choice to Plotly's expected value.
    if selected_points == "none":
        point_setting = False
    else:
        point_setting = selected_points

    # Create the seven figures in dictionary order.
    figures = []

    for variable, variable_label in distribution_variables.items():

        figure = create_distribution_figure(
            filtered_data=filtered_data,
            variable=variable,
            variable_label=variable_label,
            point_setting=point_setting
        )

        figures.append(figure)

    return (
        figures[0],  # Happiness Score
        figures[1],  # GDP
        figures[2],  # Social Support
        figures[3],  # Healthy Life Expectancy
        figures[4],  # Freedom
        figures[5],  # Generosity
        figures[6],  # Trust
        f"Report Year: {selected_year}",
        f"Countries displayed: {len(filtered_data)}"
    )

# -------------------------------------------------------------
# 22- RUN THE COMPLETE DASH APPLICATION
# -------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)