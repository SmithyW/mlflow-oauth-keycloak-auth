# mlflow-oauth-keycloak-auth
The purpose of this package is to enable the use of the [MLflow "fluent" tracking API](https://mlflow.org/docs/latest/python_api/mlflow.html) with upstream oauth2-proxy.

## Getting started

```bash
pip install mlflow-oauth-keycloak-auth
```

If not already present, mlflow obviously should be installed.

```bash
pip install mlflow
```

## Usage

```python
import mlflow
from mlflow-oauth-keycloak-auth import authentication as mlflow_auth

mlflow_auth.init()
mlflow_auth.authenticate()

# Your mlflow code
# ...

# Optional: Check the validity of the access token and refresh if it is expired
mlflow_auth.validate_or_refresh()
# Alternatively: running authenticate() again has the same effect
```

This package expects a file named `.env` in the directory your script is executed, but can be customized by creating a custom config and passing it to the `init()` method.

```python
# ...
mlflow_auth.init(env_file="/path/to/env_file")
# ...
```

## Configuration

The configuration is done exclusively via environment variables.
All of the following variables are required and can be found in the `.env.example` provided in the [Github repository file](https://github.com/SmithyW/mlflow-oauth-keycloak-auth/blob/main/.env.example).

| Variable              | Value                       | Purpose  |
| --------------------- |:---------------------------:| -----------------:|
| KMTA_CLIENT_ID        | Keycloak Client_ID          |   authentication  |
| KMTA_CLIENT_SECRET    | Keycloak Client_Secret      |   authentication  |
| KMTA_USERNAME         | Your Keycloak Username      |   authentication  |
| KMTA_PASSWORD         | Your Keycloak User Password |   authentication  |
| KMTA_TOKEN_URI        | Your Keycloak User Password |   authentication  |
| KMTA_USERINFO_URI     | Your Keycloak User Password |   check token     |


The `KMTA_TOKEN_URI` and `KMTA_USERINFO_URI` can be obtained by opening the _\<keycloak_address\>/realms/\<realm\>/.well-known/openid-configuration_ and copying the properties `token_endpoint` and `userinfo_endpoint`.
