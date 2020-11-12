from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="kampai",
      version="0.1",
      description="Data science package template generator",
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True,
      scripts=["scripts/kampai"])
