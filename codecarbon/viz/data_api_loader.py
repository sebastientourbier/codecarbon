"""
Api calls
"""
import json
import requests

API_PATH = "http://api.codecarbon.io"
USER = "jessica"
PSSD = "fake-super-secret-token"

def api_loader(fn_request_path):
    def wrapper(*args, **kwargs):
        r_path, params = fn_request_path(*args, **kwargs)
        r = requests.get(r_path, auth=(USER, PSSD), params=params)
        c = json.loads(r.content)
        return c
    return wrapper

@api_loader
def load_runs(**kwargs)->tuple:
    """
    Get all the runs

    :params:
        kwargs: can be any parameter available for the query
    """
    path = f"{API_PATH}/runs"
    return path, kwargs

@api_loader
def load_project_experiments(project_id:str, **kwargs)->tuple:
    """
    Get experiments of a given project

    :params:
        kwargs: can be any parameter available for the query

    :example:
        project_id = 'e60afa92-17b7-4720-91a0-1ae91e409ba1'
    """
    path = f"{API_PATH}/experiments/project/{project_id}"
    return path, kwargs

@api_loader
def load_experiment(experiment_id:str, **kwargs)->tuple:
    """
    Get an experiment

    :params:
        kwargs: can be any parameter available for the query

    :example:
        experiment_id = '3a202149-8be2-408c-a3d8-baeae2de2987'
    """
    path = f"{API_PATH}/experiment/{experiment_id}"
    return path, kwargs

@api_loader
def load_organization_teams(organization_id:str, **kwargs)->tuple:
    """
    Get teams of a given organization

    :params:
        kwargs: can be any parameter available for the query

    :example:
        organization_id = 'e52fe339-164d-4c2b-a8c0-f562dfce066d'
    """
    path = f"{API_PATH}/teams/organization/{organization_id}"
    return path, kwargs

@api_loader
def load_team_projects(team_id:str, **kwargs)->tuple:
    """
    Get projects of a given team

    :params:
        kwargs: can be any parameter available for the query
    """
    path = f"{API_PATH}/projects/team/{team_id}"
    return path, kwargs

@api_loader
def load_experiment_runs(experiment_id:str, **kwargs)->tuple:
    """
    Get runs of a given experiment

    :params:
        kwargs: can be any parameter available for the query

    :example:
        experiment_id = 'f52fe339-164d-4c2b-a8c0-f562dfce066d'
    """
    path = f"{API_PATH}/runs/experiment/{experiment_id}"
    return path, kwargs

@api_loader
def load_run_emissions(run_id:str, **kwargs)->tuple:
    """
    Get emissions of a given run

    :params:
        kwargs: can be any parameter available for the query

    :example:
        run_id = '58e2c11e-b91f-4adb-b0e0-7e91b72ffb80'
    """
    path = f"{API_PATH}/emissions/run/{run_id}"
    return path, kwargs


@api_loader
def load_experiment_metadata(experiment_id:str, **kwargs)->tuple:
    """
    Load run metadata of a given run

    :params:
        kwargs: can be any parameter available for the query

    :example:
        experiment_id = '58e2c11e-b91f-4adb-b0e0-7e91b72ffb80'
    """
    path = f"{API_PATH}/runs/experiment/{experiment_id}"
    return path, kwargs
