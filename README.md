
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
- kampai g pipeline // with 2 steps for debug
- kampai g transformer col_a col_b --output col_c col_d
- kampai show pipeline sample 100 // show first 100 lines transformed
- kampai g model xgboost // add xgboost model
- kampai train

=> add all sklearn features as commands?

=> setup virtual env

=> create github project / opt confirm

- kampai read a.csv analyse dataset
- kampai clean col_a --no-commit // remove null values
- kampai // standard scaler
- kampai // simple imputer

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
- generate api
- generate front
- show pred in both

- command starting a python maze allowing to trigger commands or deployments
or at least vizualize status

- make the terminal engaging, gamification on project perf ?

- provide access to generic kampai package classes in project
rails classes, not only rails command

- KAMPAI_PACKAGE_ROOT allows to trun commands from anywhere in the project structure

- no need to install the generated package in order to use the kampai scripts

- refacto : clarify the context the functions are supposed to be used in
(project generation by script, inside of project by script, inside of project by project)

- list created files at each step (kampai new, kampai generate, etc)

- activate the virtual env of the project when running a command

- clone templates from url / git version

- create framework classes
:- KampaiMLFlow
:- KampaiTrainer
:- create application.rb conf file for mlflow server source

- add tests
- validate on windows

- DE week students learn to create a template
- kampai allows to juggle with the templates and shared code and prod

- >>> use MVC pattern for command line, note for data repo

- use classes pattern : app, router, repo

- externalize templates (or just alternative ones) in separate github repos + create repo registry (hard coded vs online service) ?

# install

``` bash
pip install .
```

# usage

``` bash
kampai new PROJECT_NAME       # creates a new data science project

kampai fetch                  # retrieves csv data from url and stores it locally
                              # defaults to 1000 of taxifare

kampai head                   # displays head of fetched data

kampai train                  # trains model
```

# development

test the script locally while developping using symlink install:

``` bash
pip install -e .
```

# template parameters

## directories

KAMPAI_PACKAGE_SLUG            package_directory_name

## files

KAMPAI_PACKAGE_NAME            package_name

KAMPAI_PACKAGE_CLASS           PackageName

KAMPAI_PACKAGE_ROOT            full project root path

KAMPAI_PACKAGE_DESCRIPTION     Package description

KAMPAI_PACKAGE_SCRIPT          package_script_name
