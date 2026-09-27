FROM apache/airflow:2.9.3

USER root

# Dépendances système nécessaires pour compiler psycopg2 et autres libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Installation propre des dépendances Python (une seule fois, à la construction de l'image)
# On épingle dbt-core en plus de dbt-postgres pour éviter de récupérer une version
# récente de dbt où l'adaptateur postgres serait marqué expérimental.
RUN pip install --no-cache-dir \
    dbt-core==1.8.0 \
    dbt-postgres==1.8.0 \
    pandas \
    sqlalchemy \
    psycopg2-binary
