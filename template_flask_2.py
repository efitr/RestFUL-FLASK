from flask import Flask, request

template = Flask(__name__):

@template.route('/')
def hello_world():
    return 'Amo la vida!'

if __name__ == '__main__':
    template.run()
    template.config("DEBUG") = True
