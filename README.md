
# usage

``` bash
pip install git+https://github.com/gmanchon/kampai

kampai new PACKAGE            # creates a package boilerplate

kampai gen GIST               # generates gist code boilerplate
```

# development

test the script locally while developping using symlink install:

``` bash
pip install -e .
```

# template token replacements

## files and directories

KAMPAI_PACKAGE_NAME            package_name

## files

KAMPAI_PACKAGE_NAME            package_name

KAMPAI_PACKAGE_CLASS           PackageName

KAMPAI_PACKAGE_ROOT            full package root path

KAMPAI_PACKAGE_DESCRIPTION     Package description

KAMPAI_PACKAGE_SCRIPT          package_script_name
