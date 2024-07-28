# mlflow-oauth-keycloak-auth
The purpose of this package is to enable the use of the [MLflow "fluent" tracking API](https://mlflow.org/docs/latest/python_api/mlflow.html) with upstream oauth2-proxy.


The configuration is done exclusively via environment variables.
All of the following variables are required and can be found in the provided `.env.example` file.

| Variable              | Value                       | Purpose  |
| --------------------- |:---------------------------:| -----------------:|
| KMTA_CLIENT_ID        | Keycloak Client_ID          |   authentication  |
| KMTA_CLIENT_SECRET    | Keycloak Client_Secret      |   authentication  |
| KMTA_USERNAME         | Your Keycloak Username      |   authentication  |
| KMTA_PASSWORD         | Your Keycloak User Password |   authentication  |
| KMTA_TOKEN_URI        | Your Keycloak User Password |   authentication  |
| KMTA_USERINFO_URI     | Your Keycloak User Password |   check token     |


The `KMTA_TOKEN_URI` and `KMTA_USERINFO_URI` are the token_endpoint and userinfo_endpoint found when accessing `<keycloak_address>/realms/<realm>/.well-known/openid-configuration`.

This package expects a file named `.env`, but can be customized by creating a custom config.
