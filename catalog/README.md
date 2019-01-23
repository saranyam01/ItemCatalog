# Udacity-Item-catalog-Project
App for Item catalog project
This is a python module that creates a website and JSON API for a list of Categories and Items. 
Registered users will have ability to create, edit and delete their own items.
Each item can be created , modified or deleted by providing user authentication using Google.
This application uses Flask,SQL Alchemy, JQuery,CSS, Javascript, and OAuth2 to create Item catalog website.

### Prerequisites
You will need to install these following application in order to make this code work.
* Unix-style terminal(Windows user please download and use [Git Bash terminal](https://git-scm.com/downloads))
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Python 2.7](https://www.python.org/downloads/)
* [Sqlalchemy](https://www.sqlalchemy.org/download.html)

###You will need the following other resources for it to run:
* Flask (http://flask.pocoo.org/).
* Httplib2 (https://pypi.python.org/pypi/httplib2/0.10.3).
* Oauth2client (https://pypi.python.org/pypi/oauth2client/).
* Web browser i.e. Chrome (https://www.google.com/chrome/)

###Installation
1.virtualBox
2.Vagrant
3.python 2.7


###You will also need to download these following files to make it work.
* [VM configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)

###Instructions to Run the project

Setting up OAuth 2.0
1. You will need to signup for a google account and set up a client id and secret.
2. Visit http://console.developers.google.com for google setup.

###Setting up the Environment

1. clone or download the repo into vagrant environment.
2. Type command vagrant up,vagrant ssh.
3. In VM, cd /vagrant/catalog
4. Install Flask (http://flask.pocoo.org/) with pip install Flask, if it is not installed already.
5.  Install Sqlalchemy, Httplib2 and Oauth2client with sudo apt-get install, if they are not installed already.
6. Run python database_setup.py to create the database.
7. Run Python categoryitems.py to add the menu items
8. Run python 'project.py'
9. open your webbrowser and visit http://localhost:8000/
10. open your web browser and check for JSONS 
http://localhost:8000/catalog/JSON
http://localhost:8000/catalog/1/JSON
http://localhost:8000/items/JSON


