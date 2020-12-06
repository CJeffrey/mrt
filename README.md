## MRT Search System

### Purpose
A generic solution to find the best MRT travel plan!

### How to build and deploy
* Requirements
  * This project is tested in Python 3.9.0.

* Build
  * This is a standard Python project. You can easily build it by standard Python Packaging command, such as
    ```python setup.py sdist bdist_wheel```.

* Local Deploy
  * Simply install the built package using ```pip```.

* Docker Deploy
  * TODO

### How to use

* Use from the web
  * Run the mrt server ```python mrt.server.mrt_server```.
  * Search on the local web ```http://localhost:5000/search_basic```.

* Use as a 3rd part lib
  * call the lib in ```mrt.core```. See more pydoc inside source code for help.
 
### Test
* Unit Test
  * Based on tox. Use command ```tox``` to trigger.
  
* Frontend Test
  * TODO  

* Backend Test
  * TODO
  
* Performance Test
  * TODO
