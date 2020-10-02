
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
- kanpai g pipeline // with 2 steps for debug
- kanpai g transformer col_a col_b --output col_c col_d
- kanpai show pipeline sample 100 // show first 100 lines transformed
- kanpai g model xgboost // add xgboost model
- kanpai train

=> add all sklearn features as commands?

=> setup virtual env

=> create github project / opt confirm

- kanpai read a.csv analyse dataset
- kanpai clean col_a --no-commit // remove null values
- kanpai // standard scaler
- kanpai // simple imputer

- check invalid chars in project names (ie ds-project)

demo:
- show project status
- get data
- generate empty pipeline with 2 steps
- list pipeline columns (in, out)
- add col transformer
- affect model type
- train (locally ?) vs gcp
- save model / code / perf
- push to gcr a version of model / code / perf
- make pred
AFFICHER LE STATUS DU PROJET:
fetch > clean > preproc > train > push > pred > perf > validate
check prev step is ok
- how to retrieve the name of the package
- inject sample notebook using the projet
inject in json using popular wheel templating lib

- command starting a python maze allowing to trigger commands or deployments
or at least vizualize status

- make the terminal engaging, gamification on project perf ?

# install

``` bash
pip install .
```

# usage

``` bash
kanpai new PROJECT_NAME       # creates a new data science project

kanpai fetch                  # retrieves csv data from url and stores it locally
                              # defaults to 1000 of taxifare

kanpai head                   # displays head of fetched data
```

# development

test the script locally while developping using symlink install:

``` bash
pip install -e .
```

# template parameters

## directories

KANPAI_PACKAGE_SLUG            package_directory_name

## files

KANPAI_PACKAGE_NAME            package_name

KANPAI_PACKAGE_DESCRIPTION     Package description

KANPAI_PACKAGE_SCRIPT          package_script_name
