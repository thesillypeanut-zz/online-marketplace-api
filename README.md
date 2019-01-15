# Online Marketplace API

A simple server side web API that uses CRUD operations to query products and simulate shopping cart transactions in an online marketplace, built using the Flask microframework and SQLite database. 

## Requirements

On a Linux environment, run the following commands:
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

## Getting Started

Clone this repository:
```bash
git clone https://github.com/thesillypeanut/online-marketplace-api.git
cd online-marketplace-api/
```
Create and activate your virtual environment:
```bash
virtualenv venv
source venv/bin/activate
```
Install your project dependencies:
```bash
pip install -r requirements.txt
```
Run the code:
```bash
python3 app.py
```
To deactivate your virtual environment, run:
```bash
deactivate
```