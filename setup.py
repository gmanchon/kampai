from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="canai",
      version="0.1",
      description="Data science project template generator",
      install_requires=requirements,
      scripts=["scripts/kanpai"])
