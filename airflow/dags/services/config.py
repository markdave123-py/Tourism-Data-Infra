from airflow.models import Variable


def get_config(name, default_value=None):
    """
    Fetch configuration from Airflow Variables.
    """
    try:
        return Variable.get(name)
    except KeyError:
        if default_value is not None:
            return default_value
        raise KeyError(
            f"Airflow Variable '{name}' is not set and no default provided.")
