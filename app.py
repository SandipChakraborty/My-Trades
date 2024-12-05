from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Worldss'

# Befor pushing to git please comment the below 2 lines
# if __name__ == '__main__':
#     app.run()