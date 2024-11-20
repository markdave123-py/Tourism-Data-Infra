from airflow.models import Variable


def get_config(variable_name, default_value=None):
    """
    Fetch configuration from Airflow Variables.
    """
    try:
        return Variable.get(variable_name)
    except KeyError:
        if default_value is not None:
            return default_value
        raise KeyError(f"Airflow Variable '{variable_name}' is not set and no default value was provided.")
