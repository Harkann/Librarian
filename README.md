# Librarian

Database Project for the L3 at the ENS Paris-Saclay (2018)

## Requirements
* python >= 3.6 (might work with versions < 3.6, bt untested)
* pip3
* virtualenv

## Setup
```
git clone https://github.com/Harkann/Librarian.git
cd Librarian
virtualenv -p python3 env
source ./env/bin/activate
pip3 install requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```
We setup a virtualenv to install required packages locally.

## Running in dev
```
python3 manage.py runserver
```
You should now have a server running on localhost:8000

## Website
Everything should be almost straight forward.
You can:
* log in and out (not implemented right now)
* search for books/authors/editions/... in the database
* add new books/authors/editions/...
* leave a comment on an edition
* rate an edition
