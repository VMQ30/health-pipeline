FROM apache/airflow:2.8.1-python3.10

USER root

# Install system dependencies required for compilation and DuckDB/C++ extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements and install Python packages inside the Airflow image
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Ensure src/ is on the Python path so Airflow DAGs can import pipeline_utils
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"