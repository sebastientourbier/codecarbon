import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd
import plotly.express as px
from codecarbon.viz.data_api_loader import (
    load_experiment_runs,
    load_experiment,
    load_run_emissions,
    load_project_experiments,
)

class Components:
    def __init__(self):
        self.colorscale = [
            "rgb(0, 68, 27)",  # greens
            "rgb(0, 109, 44)",
            "rgb(35, 139, 69)",
            "rgb(65, 171, 93)",
            "rgb(116, 196, 118)",
            "rgb(161, 217, 155)",
            "rgb(199, 233, 192)",
            "rgb(229, 245, 224)",
            "rgb(240, 240, 240)",  # greys
            "rgb(217, 217, 217)",
            "rgb(189, 189, 189)",
            "rgb(253, 208, 162)",  # oranges
            "rgb(253, 174, 107)",
            "rgb(253, 141, 60)",
        ]  # px.colors.sequential.Greens_r,


    @staticmethod
    def get_experiment_input():
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.H3("Experiment id", style={"textAlign": "left"}),
                    dcc.Input(
                        id="experiment_id",
                        type="text",
                        placeholder="0bfa2432-efda-4656-bdb4-f72d15866b0b",
                    ),
                ],
                style={"display": "inline-block"},
            )
        )

    @staticmethod
    def get_header():
        return dbc.Jumbotron(
            [
                html.H1("Carbon Footprint", style={"textAlign": "center"}),
                html.P(
                    "Measure Compute Emissions",
                    style={"textAlign": "center", "paddingLeft": "0.5%"},
                    className="lead",
                ),
            ]
        )

    @staticmethod
    def get_net_summary():
        return html.Div(
            [
                html.H2("Across All Experiments", style={"textAlign": "center"}),
                html.H4(
                    [
                        "Net Power Consumption : ",
                        html.Strong(
                            id="net_power_consumption",
                            style={"fontWeight": "normal", "color": "green"},
                        ),
                    ],
                    style={"textAlign": "left", "float": "left"},
                ),
                html.H4(
                    [
                        "Net Carbon Equivalent : ",
                        html.Strong(
                            id="net_carbon_equivalent",
                            style={"fontWeight": "normal", "color": "green"},
                        ),
                    ],
                    style={"textAlign": "right", "float": "right"},
                ),
            ],
            style={"paddingLeft": "1.4%", "paddingRight": "1.4%"},
        )

    @staticmethod
    def get_experiment_dropdown():
        # PROJECT_ID = "e60afa92-17b7-4720-91a0-1ae91e409ba1"
        # PROJECT_ID = "20eaf4aa-ba1a-4f1a-9463-d680aff970bc"
        PROJECT_ID = "225904ca-f741-477c-83f5-d61587d6286c"
        experiments = load_project_experiments(PROJECT_ID)
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.H3("Select an Experiment", style={"textAlign": "left"}),
                    dcc.Dropdown(
                        id="experiment_id",
                        options=[{"label": i['name'], "value": i['id']} for i in experiments],
                        value=experiments[0],
                    ),
                ],
                style={"display": "inline-block"},
            )
        )

    @staticmethod
    def get_experiment_details():
        return html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        html.H3(
                            [
                                "Infrastructure Hosted at ",
                                html.Strong(
                                    id="experiment_infrastructure_location",
                                    style={"fontWeight": "normal", "color": "green"},
                                ),
                            ],
                            style={"float": "left"},
                        )
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.H4(
                            [
                                "Power Consumption Across All Runs : ",
                                html.Strong(
                                    id="experiment_power_consumption",
                                    style={"fontWeight": "normal", "color": "green"},
                                ),
                            ],
                            style={"float": "left"},
                        ),
                        html.H4(
                            [
                                "Last Run Power Consumption : ",
                                html.Strong(
                                    id="last_run_power_consumption",
                                    style={"fontWeight": "normal", "color": "green"},
                                ),
                            ],
                            style={"float": "right"},
                        ),
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        html.H4(
                            [
                                "Carbon Equivalent Across All Runs : ",
                                html.Strong(
                                    id="experiment_carbon_equivalent",
                                    style={"color": "green", "fontWeight": "bold"},
                                ),
                            ],
                            style={"float": "left"},
                        ),
                        html.H4(
                            [
                                "Last Run Carbon Equivalent : ",
                                html.Strong(
                                    id="last_run_carbon_equivalent",
                                    style={"fontWeight": "normal", "color": "green"},
                                ),
                            ],
                            style={"float": "right"},
                        ),
                    ]
                ),
            ],
            style={"paddingLeft": "1.4%", "paddingRight": "1.4%"},
        )

    @staticmethod
    def get_exemplary_equivalents():
        return html.Div(
            [
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.H2("Exemplary Equivalents", style={"textAlign": "center"}),
                        html.Br(),
                        html.P(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            id="house_icon",
                                            style={"height": "20%", "width": "50%"},
                                        ),
                                        html.Div(
                                            [
                                                html.Strong(
                                                    id="household_fraction",
                                                    style={
                                                        "color": "green",
                                                        "fontSize": 20,
                                                        "paddingLeft": "4%",
                                                    },
                                                ),
                                                html.H5(
                                                    "of weekly",
                                                    style={"paddingLeft": "3.5%"},
                                                ),
                                                html.H5(
                                                    "American",
                                                    style={"paddingLeft": "2.8%"},
                                                ),
                                                html.H5("household"),
                                                html.H5(
                                                    "emissions",
                                                    style={"paddingLeft": "1.4%"},
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={"float": "left", "width": "25%"},
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            id="car_icon",
                                            style={
                                                "height": "43%",
                                                "width": "28.5%",
                                                # "paddingLeft": "2%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Strong(
                                                    id="car_miles",
                                                    style={
                                                        "color": "green",
                                                        "fontWeight": "bold",
                                                        "fontSize": 20,
                                                    },
                                                ),
                                                html.H5(
                                                    "driven",
                                                    style={"paddingLeft": "5.5%"},
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "float": "left",
                                        "width": "50%",
                                        "paddingLeft": 90,
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            id="tv_icon",
                                            style={
                                                "height": "35%",
                                                "width": "53%",
                                                "paddingLeft": "5%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Strong(
                                                    id="tv_time",
                                                    style={
                                                        "color": "green",
                                                        "fontSize": 20,
                                                        "paddingLeft": "8%",
                                                    },
                                                ),
                                                html.H5(
                                                    "of 32-inch",
                                                    style={"paddingLeft": "5%"},
                                                ),
                                                html.H5(
                                                    "LCD TV",
                                                    style={"paddingLeft": "10%"},
                                                ),
                                                html.H5(
                                                    "watched",
                                                    style={"paddingLeft": "6.4%"},
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={"float": "right", "width": "25%"},
                                ),
                            ],
                            style={"paddingLeft": "20%", "paddingRight": "15%"},
                        ),
                    ],
                    style={"display": "inline-block"},
                ),
            ]
        )

    @staticmethod
    def get_cloud_emissions_comparison():
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.Br(),
                    html.H2(
                        [
                            "Emissions Across ",
                            html.Strong(
                                id="cloud_provider_name",
                                style={"fontWeight": "normal", "color": "green"},
                            ),
                            " Regions",
                        ],
                        style={"textAlign": "center", "marginLeft": "12%"},
                    ),
                    dcc.Graph(id="cloud_emissions_barchart"),
                    html.Br(),
                    html.Div(
                        id="cloud_recommendation",
                        style={"marginLeft": "12%", "textAlign": "center"},
                    ),
                ],
                id="cloud_emissions_comparison_component",
            ),
            style={"marginLeft": "-12%"},
        )

    def get_cloud_emissions_barchart_figure(
        self, cloud_emissions_barchart_data: pd.DataFrame
    ):
        return (
            px.bar(
                cloud_emissions_barchart_data,
                x="region",
                y="emissions",
                hover_data=["region", "countryName", "emissions"],
                color="emissions",
                labels={
                    "emissions": "Carbon Equivalent (kg)",
                    "region": "Region",
                    "countryName": "Country",
                },
                color_continuous_scale=self.colorscale,
                height=500,
                width=1400,
            )
            .update_xaxes(tickangle=45)
            .update_layout(plot_bgcolor="rgb(255,255,255)")
        )

    def get_cloud_recommendation(
        self,
        on_cloud: str,
        cloud_provider_name: str,
        cloud_emissions_barchart_data: pd.DataFrame,
    ):
        if on_cloud == "N":
            return html.H4()
        cloud_emissions_experiment_region = cloud_emissions_barchart_data.iloc[0, :]
        cloud_emissions_minimum_region = cloud_emissions_barchart_data.iloc[1, :]
        if (
            cloud_emissions_minimum_region.emissions
            > cloud_emissions_experiment_region.emissions
        ):
            return html.H4(
                [
                    f"Already running on {cloud_provider_name}'s least emissions region ",
                    html.Strong(
                        f"{cloud_emissions_experiment_region.region}",
                        style={"fontWeight": "normal", "color": "green"},
                    ),
                ]
            )
        else:
            return (
                html.H4(
                    [
                        "Had this been run in ",
                        html.Strong(
                            f"{cloud_emissions_minimum_region.region}",
                            style={"fontWeight": "normal", "color": "green"},
                        ),
                        " region, ",
                    ]
                ),
                html.H4(
                    [
                        "then the emitted carbon would have been ",
                        html.Strong(
                            f"{'{:.1f}'.format(cloud_emissions_minimum_region.emissions)} kg",
                            style={"fontWeight": "normal", "color": "green"},
                        ),
                    ]
                ),
                html.H4(
                    [
                        "Reducing the current  emissions by ",
                        html.Strong(
                            f"{'{:.1f}'.format(cloud_emissions_experiment_region.emissions - cloud_emissions_minimum_region.emissions)} kg",
                            style={"fontWeight": "normal", "color": "green"},
                        ),
                    ]
                ),
            )

    @staticmethod
    def get_emissions_tab():
        return dcc.Tab(
            label="Emissions Equivalent",
            value="emissions_tab",
            id="global_emissions",
            children=[
                html.Div(
                    dbc.Col(
                        dcc.Graph(id="global_emissions_choropleth"),
                        style={"marginLeft": "-16%"},
                    )
                )
            ],
        )

    @staticmethod
    def get_energy_mix_tab():
        return dcc.Tab(
            label="Energy Mix",
            value="energy_mix_tab",
            id="global_energy_mix",
            children=[
                html.Div(
                    dbc.Col(
                        [
                            html.Br(),
                            html.H4("Select Energy Source"),
                            dcc.Dropdown(
                                id="energy_type",
                                options=[
                                    {"label": "Coal", "value": "coal"},
                                    {"label": "Petroleum", "value": "petroleum"},
                                    {"label": "Natural Gas", "value": "natural_gas"},
                                    {"label": "Low Carbon", "value": "low_carbon"},
                                ],
                                value="coal",
                            ),
                            dcc.Graph(
                                id="global_energy_mix_choropleth",
                                style={"marginLeft": "-16%"},
                            ),
                        ]
                    )
                )
            ],
        )

    def get_global_comparison(self):
        return html.Div(
            [
                html.Br(),
                html.Br(),
                html.H2(
                    "Global Benchmarks",
                    style={
                        "textAlign": "center",
                        "paddingLeft": "15%",
                        "marginLeft": "-15%",
                    },
                ),
                html.Br(),
                html.Br(),
                dcc.Tabs(
                    id="global_benchmarks",
                    value="emissions_tab",
                    children=[self.get_emissions_tab(), self.get_energy_mix_tab()],
                ),
            ]
        )

    def get_global_emissions_choropleth_figure(self, choropleth_data):
        return px.choropleth(
            data_frame=choropleth_data,
            locations="iso_code",
            color="emissions",
            hover_data=[
                "country",
                "emissions",
                "coal",
                "petroleum",
                "natural_gas",
                "low_carbon",
            ],
            labels={
                "country": "Country",
                "emissions": "Carbon Equivalent (kg)",
                "iso_code": "Country Code",
                "coal": "Coal Energy (%)",
                "petroleum": "Petroleum Energy (%)",
                "natural_gas": "Natural Gas Energy (%)",
                "low_carbon": "Low Carbon Energy (%)",
            },
            width=1400,
            height=600,
            color_continuous_scale=self.colorscale,
        )

    def get_global_energy_mix_choropleth_figure(self, energy_type, choropleth_data):
        energy_labels = {
            "coal": "Coal Energy (%)",
            "petroleum": "Petroleum Energy (%)",
            "natural_gas": "Natural Gas Energy (%)",
            "low_carbon": "Low Carbon Energy (%)",
        }
        return px.choropleth(
            data_frame=choropleth_data,
            locations="iso_code",
            color=energy_type,
            hover_data=["country", "emissions", energy_type],
            labels={
                "country": "Country",
                "emissions": "Carbon Equivalent (kg)",
                "iso_code": "Country Code",
                energy_type: energy_labels[energy_type],
            },
            width=1400,
            height=600,
            color_continuous_scale=list(reversed(self.colorscale))
            if energy_type == "low_carbon"
            else self.colorscale,
        )

    @staticmethod
    def get_regional_emissions_comparison():
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.Br(),
                    html.H2(
                        [
                            "Emissions Across Regions in ",
                            html.Strong(
                                id="country_name",
                                style={"fontWeight": "normal", "color": "green"},
                            ),
                        ],
                        style={"textAlign": "center", "marginLeft": "12%"},
                    ),
                    dcc.Graph(id="regional_emissions_comparison_choropleth"),
                ],
                id="regional_emissions_comparison_component",
            ),
            style={"marginLeft": "-12%"},
        )

    def get_regional_emissions_choropleth_figure(
        self, choropleth_data, country_iso_code: str
    ):
        # add location_modes and scopes for other country codes
        location_modes = {"usa": "USA-states", "can": "geojson-id"}
        scopes = {"usa": "usa", "can": "north america"}
        locations = {"usa": "region_code", "can": "cartodb_id"}

        # formatting required for geojson data (not required for USA regional map)
        if country_iso_code.lower() == "can":
            with open("codecarbon/data/canada_provinces.geojson", "r") as geo:
                mp = json.load(geo)
            for choropleth in choropleth_data:
                region_name = choropleth["region_code"]
                choropleth["cartodb_id"] = [
                    m["properties"]["cartodb_id"]
                    for m in mp["features"]
                    if m["properties"]["name"].lower() == region_name
                ][0]
        else:
            mp = None

        # Get parameters, default to a blank world map if not in keys
        location_mode = location_modes.get(country_iso_code.lower(), None)
        scope = scopes.get(country_iso_code.lower(), "world")
        location = locations.get(country_iso_code.lower(), None)

        fig = px.choropleth(
            data_frame=choropleth_data,
            locations=location,
            geojson=mp,
            featureidkey="properties.cartodb_id",
            locationmode=location_mode,
            scope=scope,
            color="emissions",
            hover_data=["region_name", "emissions", "region_code"],
            labels={
                "region_name": "Region",
                "emissions": "Carbon Equivalent (kg)",
                "region_code": "Region Code",
            },
            width=1400,
            height=600,
            color_continuous_scale=self.colorscale,
        )
        if country_iso_code.lower() != "usa":
            fig.update_geos(fitbounds="locations", visible=True)
        return fig

    @staticmethod
    def get_experiment_time_series():
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.Br(),
                    html.H2("Emissions Timeline", style={"textAlign": "center"}),
                    dcc.Graph(id="experiment_time_series"),
                ]
            ),
            style={"paddingLeft": "3%"},
        )

    @staticmethod
    def get_experiment_emissions_bar_chart():
        return html.Div(
            dbc.Col(
                [
                    html.Br(),
                    html.Br(),
                    html.H2("Emissions Detail", style={"textAlign": "center"}),
                    dcc.Graph(id="experiment_emissions_bar_chart"),
                ]
            ),
            style={"paddingLeft": "3%"},
        )

    @staticmethod
    def get_experiment_time_series_figure(experiment_data: dt.DataTable):
        return (
            px.line(
                experiment_data,
                x="timestamp",
                y="emissions",
                hover_data=["emissions"],
                labels={
                    "emissions": "Carbon Equivalent (kg)",
                    "timestamp": "Timestamp",
                },
            )
            .update_traces(line_color="green")
            .update_layout(plot_bgcolor="rgb(255,255,255)")
        )

    @staticmethod
    def get_experiment_emissions_bar_chart_figure(experiment_data: dt.DataTable):
        # Note: necessary to both convert to pandas and replace null values for hover value
        experiment_data = pd.DataFrame(experiment_data)
        experiment_data = experiment_data.replace(np.nan, "", regex=True)
        hover_data = {c: True for c in experiment_data.columns}
        bar = (
            px.bar(
                experiment_data,
                y="emissions",
                hover_data=hover_data,
                labels={
                    "emissions": "Carbon Equivalent (kg)",
                    "energy_consumed": "Energy Consumed (kWh)",
                    "timestamp": "Timestamp",
                    "experiment_id": "Experiment Name",
                    "duration": "Duration",
                    "emissions_detail": "Emissions Detail",
                    "country_name": "Country Name",
                    "country_iso_code": "Country ISO Code",
                    "region": "Region",
                    "cloud_provider": "Cloud Provider",
                    "cloud_region": "Cloud Region",
                },
            )
            .update_traces(marker_color="green")
            .update_layout(plot_bgcolor="rgb(255,255,255)")
        )
        return bar

    @staticmethod
    def get_hidden_experiment_data():
        return html.Div(id="hidden_experiment_data", style={"display": "none"})

    @staticmethod
    def get_hidden_experiment_summary():
        return html.Div(
            dcc.Store(id="hidden_experiment_summary"), style={"display": "none"}
        )

    @staticmethod
    def get_references():
        return html.Div(
            [
                html.Br(),
                html.Br(),
                html.H2("References "),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "Energy Usage Reports: Environmental awareness as part of algorithmic accountability",
                                href="https://arxiv.org/pdf/1911.08354.pdf",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Quantifying the Carbon Emissions of Machine Learning",
                                href="https://arxiv.org/pdf/1910.09700.pdf",
                            )
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
            ]
        )

    @staticmethod
    def get_runs(experiment_id: str) -> pd.DataFrame:
        if not experiment_id: # or len(experiment_id) != 36:
            raise PreventUpdate

        runs_from_api = load_experiment_runs(experiment_id)
        print("type", type(runs_from_api))
        print("runs!", runs_from_api)

        if not runs_from_api:
            raise PreventUpdate("Invalid experiment id")

        # runs = [run['id'] for run in runs_from_api]
        return runs_from_api

    @staticmethod
    def get_experiment(experiment_id: str) -> pd.DataFrame:
        """
        Retrieve experiment

        1. get id of all the runs for the experiment
        2. get data of the runs (using their id)
        3. aggregate
        """
        experiment_runs = load_experiment_runs(experiment_id)
        run_ids = [run_meta_data['id'] for run_meta_data in experiment_runs]
        runs = []
        for run_id in run_ids:
            runs = runs + load_run_emissions(run_id)['items']

        cols = [col for col in runs[0]]
        print(cols)
        print("\n\n\n\n\n\n")

        df_runs = pd.DataFrame(runs, columns=cols)

        # TODO: modify to have the same shape than the csv dataframe
        return df_runs
