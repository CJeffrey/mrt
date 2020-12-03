from setuptools import setup, find_packages

setup(
    name='mrt',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Flask~=1.1.2',
    ]
)