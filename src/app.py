
from flask import Flask
from CoverageSearch import CoverageSearchApi
#import createTable
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

def page_not_found(error):
    return "<h1>Page not found D:</h1>", 404

if __name__ == '__main__':
    #createTable.try_build_db()
    app.register_blueprint(CoverageSearchApi.main, url_prefix='/coverage')

    app.register_error_handler(404, page_not_found)
    app.run(use_reloader=False)
