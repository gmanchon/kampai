
# todo

let constructing a ds project boilerplate the goal of the de week
let this package automate it once teached

allow user to input parameters for gcp and other cloud providers
... or use gcloud command to retrieve them?

allow user to select a base template:
- front web: streamlit
- front api: fastapi, flask
- back pred ml: gcr, gke
- back pred deep: gke
- back train: gaip

allow user to create sklearn pipeline and transformers
- canai g pipeline // with 2 steps for debug
- canai g transformer col_a col_b --output col_c col_d
- canai show pipeline sample 100 // show first 100 lines transformed
- canai g model xgboost // add xgboost model
- canai train

=> add all sklearn features as commands?

=> setup virtual env

=> create github project / opt confirm

- canai read a.csv analyse dataset
- canai clean col_a --no-commit // remove null values
- canai // standard scaler
- canai // simple imputer

# install

``` bash
pip install .
```

# usage

``` bash
canai new PROJECT_NAME
```

# development

test the script locally while developping using symlink install:

``` bash
pip install -e .
```

# template parameters

## directories

CANAI_PACKAGE_SLUG            package_directory_name

## files

CANAI_PACKAGE_NAME            package_name

CANAI_PACKAGE_DESCRIPTION     Package description

CANAI_PACKAGE_SCRIPT          package_script_name
