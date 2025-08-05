from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="E-COMMERCE BASED RECOMMENDER",
    version="0.1",
    author="Gouranga",
    packages=find_packages(),
    install_requires = requirements,
)