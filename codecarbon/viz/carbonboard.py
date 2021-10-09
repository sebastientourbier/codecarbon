import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dt
import fire
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from codecarbon.viz.components import Components
from codecarbon.viz.data import Data

def adapt_new_version(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adapt DataFrame (from csv) to new system
    by renaming "experiment" into "run" and "project" into "experiment"
    and "experiment_name" into "experiment_id"
    """
    # df['']=='project*' => 'experiment*'
    # TODO: continue to implement modifications
    df.rename(columns={"experiment_name":"experiment_id"}, inplace=True)
    return df

def render_app(df: pd.DataFrame):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

    components = Components()
    header = components.get_header()
    net_summary = components.get_net_summary()
    experiment_dropdown = components.get_experiment_dropdown()
    experiment_details = components.get_experiment_details()
    exemplary_equivalents = components.get_exemplary_equivalents()
    _hidden_experiment_data = components.get_hidden_experiment_data()
    _hidden_experiment_summary = components.get_hidden_experiment_summary()
    cloud_emissions_comparison = components.get_cloud_emissions_comparison()
    global_comparison = components.get_global_comparison()
    regional_comparison = components.get_regional_emissions_comparison()
    experiment_time_series = components.get_experiment_time_series()
    experiment_emissions_bar_chart = components.get_experiment_emissions_bar_chart()
    references = components.get_references()

    data = Data()

    app.layout = dbc.Container(
        [
            header,
            net_summary,
            experiment_dropdown,
            experiment_details,
            exemplary_equivalents,
            cloud_emissions_comparison,
            global_comparison,
            regional_comparison,
            experiment_time_series,
            experiment_emissions_bar_chart,
            references,
            _hidden_experiment_data,
            _hidden_experiment_summary,
        ],
        style={"padding-top": "50px"},
    )

    @app.callback(
        [
            Output(component_id="hidden_experiment_data", component_property="children"),
            Output(component_id="hidden_experiment_summary", component_property="data"),
            Output(component_id="net_power_consumption", component_property="children"),
            Output(component_id="net_carbon_equivalent", component_property="children"),
            Output(
                component_id="experiment_infrastructure_location",
                component_property="children",
            ),
            Output(
                component_id="experiment_power_consumption", component_property="children"
            ),
            Output(
                component_id="experiment_carbon_equivalent", component_property="children"
            ),
            Output(
                component_id="last_run_power_consumption", component_property="children"
            ),
            Output(
                component_id="last_run_carbon_equivalent", component_property="children"
            ),
        ],
        [Input(component_id="experiment_id", component_property="value")],
    )
    def update_experiment_data(experiment: dict):
        # Get experiment data from api or csv
        if not experiment:
            raise PreventUpdate

        if df.empty:
            experiment_df = components.get_experiment(experiment['id'])
        else:
            experiment_df = df[df.experiment_id == experiment['id']]

        experiment_data = data.format_experiment_df(experiment_df)
        experiment_summary = data.get_experiment_summary(experiment['id'], experiment_data.data)

        #TODO: Correct issues working with csv
        print('\n\n\n')
        print(experiment_summary)
        print('\n\n\n')
        net_power_consumption = f"{'{:.1f}'.format(experiment_summary['total']['energy_consumed'])} kWh"
        net_carbon_equivalent = f"{'{:.1f}'.format(experiment_summary['total']['emissions'])} kg"
        if {experiment_summary["region"]} == "":
            experiment_infrastructure_location = f"{experiment_summary['country_name']}"
        else:
            experiment_infrastructure_location = (
                f"{experiment_summary['region']}, {experiment_summary['country_name']}"
            )
        experiment_power_consumption = (
            f"{round(experiment_summary['total']['energy_consumed'],1)} kWh"
        )
        experiment_carbon_equivalent = (
            f"{round(experiment_summary['total']['emissions'],1)} kg"
        )
        last_run_power_consumption = (
            f"{experiment_summary['last_run']['energy_consumed']} kWh"
        )
        last_run_carbon_equivalent = f"{experiment_summary['last_run']['emissions']} kg"

        return (
            experiment_data,
            experiment_summary,
            net_power_consumption,
            net_carbon_equivalent,
            experiment_infrastructure_location,
            experiment_power_consumption,
            experiment_carbon_equivalent,
            last_run_power_consumption,
            last_run_carbon_equivalent,
        )

    @app.callback(
        [
            Output(component_id="house_icon", component_property="src"),
            Output(component_id="car_icon", component_property="src"),
            Output(component_id="tv_icon", component_property="src"),
            Output(component_id="car_miles", component_property="children"),
            Output(component_id="tv_time", component_property="children"),
            Output(component_id="household_fraction", component_property="children"),
        ],
        [Input(component_id="hidden_experiment_summary", component_property="data")],
    )
    def update_exemplary_equivalents(hidden_experiment_summary: dcc.Store):
        experiment_carbon_equivalent = hidden_experiment_summary["total"]["emissions"]
        house_icon = app.get_asset_url("house_icon.png")
        car_icon = app.get_asset_url("car_icon.png")
        tv_icon = app.get_asset_url("tv_icon.png")
        car_miles = f"{data.get_car_miles(experiment_carbon_equivalent)} miles"
        tv_time = data.get_tv_time(experiment_carbon_equivalent)
        household_fraction = (
            f"{data.get_household_fraction(experiment_carbon_equivalent)} %"
        )
        return house_icon, car_icon, tv_icon, car_miles, tv_time, household_fraction

    @app.callback(
        [
            Output(
                component_id="global_emissions_choropleth", component_property="figure"
            ),
            Output(
                component_id="global_energy_mix_choropleth", component_property="figure"
            ),
        ],
        [
            Input(component_id="hidden_experiment_summary", component_property="data"),
            Input(component_id="energy_type", component_property="value"),
        ],
    )
    def update_global_comparisons(hidden_experiment_summary: dcc.Store, energy_type: str):
        if not hidden_experiment_summary: # or len(experiment_id) != 36:
            raise PreventUpdate

        net_energy_consumed = hidden_experiment_summary["total"]["energy_consumed"]
        global_emissions_choropleth_data = data.get_global_emissions_choropleth_data(
            net_energy_consumed
        )

        return (
            components.get_global_emissions_choropleth_figure(
                global_emissions_choropleth_data
            ),
            components.get_global_energy_mix_choropleth_figure(
                energy_type, global_emissions_choropleth_data
            ),
        )

    @app.callback(
        Output(
            component_id="regional_emissions_comparison_component",
            component_property="style",
        ),
        [Input(component_id="hidden_experiment_summary", component_property="data")],
    )
    def update_show_regional_comparison(hidden_experiment_summary: dcc.Store):
        country_iso_code = hidden_experiment_summary["country_iso_code"]
        # add country codes here to render for different countries
        if country_iso_code.upper() in ["USA", "CAN"]:
            return {"display": "block"}
        else:
            return {"display": "none"}

    @app.callback(
        [
            Output(component_id="country_name", component_property="children"),
            Output(
                component_id="regional_emissions_comparison_choropleth",
                component_property="figure",
            ),
        ],
        [Input(component_id="hidden_experiment_summary", component_property="data")],
    )
    def update_regional_comparison_choropleth(hidden_experiment_summary: dcc.Store):
        country_name = hidden_experiment_summary["country_name"]
        country_iso_code = hidden_experiment_summary["country_iso_code"]
        net_energy_consumed = hidden_experiment_summary["total"]["energy_consumed"]
        regional_emissions_choropleth_data = (
            data.get_regional_emissions_choropleth_data(
                net_energy_consumed, country_iso_code
            )
        )

        return (
            country_name,
            components.get_regional_emissions_choropleth_figure(
                regional_emissions_choropleth_data, country_iso_code
            ),
        )

    @app.callback(
        Output(component_id="experiment_time_series", component_property="figure"),
        [Input(component_id="hidden_experiment_data", component_property="children")],
    )
    def update_experiment_time_series(hidden_experiment_data: dt.DataTable):
        return components.get_experiment_time_series_figure(
            hidden_experiment_data["props"]["data"]
        )

    @app.callback(
        Output(component_id="experiment_emissions_bar_chart", component_property="figure"),
        [Input(component_id="hidden_experiment_data", component_property="children")],
    )
    def update_experiment_bar_chart(hidden_experiment_data: dt.DataTable):
        return components.get_experiment_emissions_bar_chart_figure(
            hidden_experiment_data["props"]["data"]
        )

    @app.callback(
        Output(
            component_id="cloud_emissions_comparison_component",
            component_property="style",
        ),
        [Input(component_id="hidden_experiment_summary", component_property="data")],
    )
    def update_on_cloud(hidden_experiment_summary: dcc.Store):
        on_cloud = hidden_experiment_summary["on_cloud"]
        if on_cloud == "Y":
            return {"display": "block"}
        else:
            return {"display": "none"}

    @app.callback(
        [
            Output(component_id="cloud_provider_name", component_property="children"),
            Output(
                component_id="cloud_emissions_barchart", component_property="figure"
            ),
            Output(component_id="cloud_recommendation", component_property="children"),
        ],
        [Input(component_id="hidden_experiment_summary", component_property="data")],
    )
    def update_cloud_emissions_barchart(hidden_experiment_summary: dcc.Store):
        on_cloud = hidden_experiment_summary["on_cloud"]
        net_energy_consumed = hidden_experiment_summary["total"]["energy_consumed"]
        cloud_provider = hidden_experiment_summary["cloud_provider"]
        cloud_region = hidden_experiment_summary["cloud_region"]
        (
            cloud_provider_name,
            cloud_emissions_barchart_data,
        ) = data.get_cloud_emissions_barchart_data(
            net_energy_consumed, on_cloud, cloud_provider, cloud_region
        )

        return (
            cloud_provider_name,
            components.get_cloud_emissions_barchart_figure(
                cloud_emissions_barchart_data
            ),
            components.get_cloud_recommendation(
                on_cloud, cloud_provider_name, cloud_emissions_barchart_data
            ),
        )

    return app


def viz(filepath: str = None, port: int = 8050, debug: bool = False) -> None:
    if filepath:
        df = pd.read_csv(filepath)
        df = adapt_new_version(df)
    else:
        df = pd.DataFrame()
    app = render_app(df)
    app.run_server(port=port, debug=debug)


def main():
    fire.Fire(viz)


if __name__ == "__main__":
    main()
