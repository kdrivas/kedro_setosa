# kedro_iris

## Overview

This is your new Kedro project, which was generated using `Kedro 0.17.5`.

This is a toy project using iris data and a random forest classifier

## Pipeline

<img src="docs/kedro-pipeline.png">

## Running Kedro on your local machine

You can run your Kedro project with:

```
kedro install
kedro run
```

## Running Kedro on airflow

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
kedro package
astro dev start
```

