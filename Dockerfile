FROM quay.io/astronomer/ap-airflow:2.0.0-buster-onbuild

RUN pip install --user src/dist/kedro_iris-0.1-py3-none-any.whl