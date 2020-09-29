from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="CANAI_PACKAGE_NAME",
      version="1.0",
      description="CANAI_PACKAGE_DESCRIPTION",
      packages=find_packages(),
      install_requires=requirements,
      scripts=["scripts/CANAI_PACKAGE_SCRIPT"])
