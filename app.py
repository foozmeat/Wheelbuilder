import os

from flask import Flask
from flask import render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from wb.forms import SearchForm
from wb.models import metadata, Rims

app = Flask(__name__)
config = os.environ.get('WB_CONFIG', 'config.DevelopmentConfig')
app.config.from_object(config)

if app.config['SENTRY_DSN']:
    from raven.contrib.flask import Sentry

    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

db = SQLAlchemy(metadata=metadata)
db.init_app(app)

ITEMS_PER_PAGE = 20


@app.before_request
def before_request():
    try:
        db.engine.execute('SELECT 1 from rims')
    except exc.SQLAlchemyError as e:
        return f"{e}<br>Wheelbuilder is unavailable at the moment", 503

    app.logger.info(session)


@app.route('/')
def index():
    return render_template('index.html.j2')


@app.route('/rims/list')
@app.route('/rims/list/<int:page>')
def rims_list(page=1):
    rims = db.session.query(Rims)

    form = SearchForm(request.args)
    if form.validate():

        size = form.size.data
        search = form.search.data

        if size:
            rims = rims.filter(Rims.size == size)

        if search:
            rims = rims.filter(Rims.description.like(f"%{search}%"))

    else:
        for e in form.errors.items():
            app.logger.error(e)

    rims = rims.order_by(Rims.description.asc()).paginate(page=page, per_page=ITEMS_PER_PAGE)

    return render_template('_rims_table.html.j2',
                           rims_paginated=rims,
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404


if __name__ == '__main__':
    app.run()
