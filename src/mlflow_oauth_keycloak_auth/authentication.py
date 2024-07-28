"""Class for fetching and storing keycloak tokens as well as setting the access token as
an environment variable (MLFLOW_TRACKING_TOKEN) for the oauth2-proxy instance to route
to keycloak. The mlflow API will append the Bearer Token in each request.
    """
import os
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from .exceptions import MissingEnvironmentVariableException

DEFAULT_ENV_FILE = ".env"
MIN_REQUIRED_VARS = ["KMTA_CLIENT_ID", "KMTA_CLIENT_SECRET",
                     "KMTA_USERNAME", "KMTA_PASSWORD", "KMTA_TOKEN_URI", "KMTA_USERINFO_URI"]
SKIP_REQUEST_ENV_VARS = ["KMTA_TOKEN_URI", "KMTA_USERINFO_URI"]


def init(*required_vars, env_file=None):
    """Initialize the environment variables by loading them either from the
    default .env file or user specified file. The function will raise an
    exception if any of the required environment variables are missing.

    Args:
        env_file (string, optional): Path to the custom environment file. Defaults to None.

    Raises:
        MissingEnvironmentVariableException: Raised when a required environment variable is missing
    """
    required_vars = set(MIN_REQUIRED_VARS +
                        (list(required_vars) if required_vars else []))

    load_dotenv(env_file or DEFAULT_ENV_FILE)
    print(
        f"Successfully loaded environment variables from {env_file or DEFAULT_ENV_FILE}")
    for var in required_vars:
        value = os.getenv(var)
        if value is None:
            raise MissingEnvironmentVariableException(var)

    print("All required environment variables are set")


def authenticate():
    """Fetch access and refresh token from keycloak"""

    uri = os.environ["KMTA_TOKEN_URI"]
    print(f"Fetching token from {uri}")

    response = requests.post(
        uri,
        data={
            "client_id": os.environ["KMTA_CLIENT_ID"],
            "client_secret": os.environ["KMTA_CLIENT_SECRET"],
            "grant_type": "password",
            "scope": "openid",
            "username": os.environ["KMTA_USERNAME"],
            "password": os.environ["KMTA_PASSWORD"]
        }, timeout=5)

    if response.status_code == 200:
        print("Successfully fetched token")
        res = response.json()
        access_token = res["access_token"]
        _set_tracking_token(access_token, res["refresh_token"])
    else:
        print("Failed to fetch token")
        raise RequestException("Failed to fetch token")


def validate_or_refresh():
    """Checks if the access token is still valid by sending a request to
    the keycloak userinfo endpoint.
    """
    uri = os.environ["KMTA_USERINFO_URI"]
    print(f"Validating token at {uri}")

    headers = {
        "Authorization": f"Bearer {os.environ['MLFLOW_TRACKING_TOKEN']}"
    }
    response = requests.get(uri, headers=headers, timeout=5)
    if response.status_code == 200:
        print("Token is still valid")
        return True

    # If the access token is invalid, try to refresh it
    print("Token is invalid, refreshing")

    data = {
        "client_id": os.environ["KMTA_CLIENT_ID"],
        "client_secret": os.environ["KMTA_CLIENT_SECRET"],
        "grant_type": "refresh_token",
        "refresh_token": os.environ["KMTA_RFTK"]
    }

    uri = os.environ["KMTA_TOKEN_URI"]
    response = requests.post(uri, data=data, timeout=5)

    if response.status_code == 200:
        res = response.json()
        access_token = res["access_token"]
        refresh_token = res["refresh_token"]
        _set_tracking_token(access_token, refresh_token)
        print("Successfully refreshed token")
        return True
    print("Failed to refresh token. Please re-authenticate")
    raise RequestException("Failed to refresh token. Please re-authenticate")


def _set_tracking_token(access_token, refresh_token=None):
    """Set the access token as an environment variable
    for the mlflow package to use when trying to connect
    to the tracking server

    Args:
        access_token (string): JWT access token
        refresh_token (string, optional): JWT refresh token. Defaults to None.
    """
    os.environ["MLFLOW_TRACKING_TOKEN"] = access_token
    if refresh_token:
        os.environ["KMTA_RFTK"] = refresh_token
