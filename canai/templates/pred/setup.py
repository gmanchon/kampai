from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="KANPAI_PACKAGE_NAME",
      version="1.0",
      description="KANPAI_PACKAGE_DESCRIPTION",
      packages=find_packages(),
      install_requires=requirements)
