from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import os
from wb.models import metadata

app = Flask(__name__)
config = os.environ.get('WB_CONFIG', 'config.DevelopmentConfig')
app.config.from_object(config)

if app.config['SENTRY_DSN']:
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

db = SQLAlchemy(metadata=metadata)
db.init_app(app)


@app.before_request
def before_request():
    try:
        db.engine.execute('SELECT 1 from rims')
    except exc.SQLAlchemyError as e:
        return f"{e}    Wheelbuilder is unavailable at the moment", 503

    app.logger.info(session)


@app.route('/')
def index():
    return 'Hello, World!'


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html.j2'), 404


if __name__ == '__main__':

    app.run()
