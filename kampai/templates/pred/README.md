
# about

[kampai](https://github.com/gmanchon/kampai) generated boilerplate code

# usage

## project generation

``` bash
kampai gen make               # generate Makefile
kampai gen test               # generate tests
kampai gen script             # generate script boilerplate
kampai gen ci                 # generate github ci conf
kampai gen registry           # generate code to log to mlflow
                              # the params, hyperparams and metrics of a run
                              # and to gcs the trained model
```

## model training

``` bash
python -m KAMPAI_PACKAGE_NAME.app
```
