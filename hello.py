"""Create a simple hello world file"""
from flask import Flask
APP = Flask(__name__)

@APP.route('/')
def say_hello():
    """ Return Hello World greeting"""
    return "Hello World"

if __name__ == '__main__':
    APP.run()
