If a secrets backend is being used for Airflow Connections, Configurations, or Variables - you can follow the instructions to [Configure a Secrets Backend](secrets-backend.md).

Typically, this involves setting the environment keys `AIRFLOW__SECRETS__BACKEND` and `AIRFLOW__SECRETS__BACKEND_KWARGS`, which are frequently set in the `Dockerfile` or [Environment Variables](environment-variables.md) in an Astro Project.
