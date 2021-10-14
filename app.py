from logging import debug
from flask import Flask
from flask import render_template
from flask import request
from scraper import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        scraper = BookScraper()
        scraper.run()
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

