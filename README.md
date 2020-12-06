# MRT Search System

## Purpose
A generic solution to find the best MRT travel plan!

## How to build and deploy
### Requirements
  * This project is tested in Python 3.9.0.

### Build
This is a standard Python project. You can easily build it by standard Python Packaging command.
1. Go to the root dir of the project
1. Install ```pip install twine~=3.2.0```
1. Run command ```python setup.py sdist bdist_wheel```.

### Local Deploy
1. Simply install the built package using ```pip install mrt-<version_number>-py3-none-any.whl```.
2. Run command ```mrt```

### Docker Deploy
1. Build docker image by the ```Dockerfile``` in project root dir
1. Simply start the docker container by the docker image

## How to use

* Use from the web
  * Search on the local web ```http://<host>:5000/```.

* Use as a 3rd part lib
  * call the lib in ```mrt.core```. See more pydoc inside source code for help.
 
## Test
### Unit & Backend Test
Based on tox. Steps to run:
1. Create a clean Python virtualenv
1. Go to the root dir of the project
1. Install requirement ```pip install -r test/unit/requirements.txt```
1. Run test by command ```tox```

### Frontend Test
Based on Selenium. Steps to run:
1. Install the test browser on your host machine
1. Download corresponding Selenium browser driver and save in ```test/frontend/drivers```. See more details in [Selenium Doc](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)
1. Create a clean Python virtualenv
1. Go to the root dir of the project
1. Install requirement ```pip install -r test/frontend/requirements.txt```
1. Run test by command ```py.test test/frontend```
  
### Performance Test
* TODO
