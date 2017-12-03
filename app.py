import logging
import os

from flask import Flask, redirect, url_for
from flask import render_template, session, request, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from wb.forms import SearchForm, BuilderForm
from wb.models import metadata, Rims, Hubs, Mru, Wheel, spoke_lengths

app = Flask(__name__)
config = os.environ.get('WB_CONFIG', 'config.DevelopmentConfig')
app.config.from_object(config)
app.logger.setLevel(logging.DEBUG)

if app.config['SENTRY_DSN']:
    from raven.contrib.flask import Sentry

    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

db = SQLAlchemy(metadata=metadata)
db.init_app(app)

ITEMS_PER_PAGE = 20


def bform(data=None):
    app.logger.info(session)

    b = BuilderForm(data,
                    hub_field=session['wheel']['hub_id'],
                    rim_field=session['wheel']['rim_id'],
                    spoke_field=session['wheel']['spokes'],
                    pattern_field=session['wheel']['pattern'],
                    nipple_length_field=session['wheel']['nipple_length'],
                    )

    b.hub_field.choices = session['hub_mru']
    b.rim_field.choices = session['rim_mru']

    return b


@app.before_request
def before_request():
    try:
        db.engine.execute('SELECT 1 from rims')
    except exc.SQLAlchemyError as e:
        return f"{e}<br>Wheelbuilder is unavailable at the moment", 503

    if 'wheel' not in session:
        session['wheel'] = Wheel().__dict__

    if 'rim_mru' not in session:
        session['rim_mru'] = []

    if 'hub_mru' not in session:
        session['hub_mru'] = []


@app.route('/')
def index():

    g.bform = bform()
    return render_template('index.html.j2')


@app.route('/wheel', methods=["POST"])
def wheel():
    app.logger.info(session)

    b_form = bform(request.form)

    if b_form.validate():

        if b_form.hub_field.data != session['wheel']['hub_id']:

            try:
                hub = db.session.query(Hubs).filter_by(id=b_form.hub_field.data).first()
                session['wheel']['hub_id'] = hub.id
                session['hub'] = hub.as_dict()

                mru = Mru(session['hub_mru'])
                mru.add(hub.mru_props)
                session['hub_mru'] = mru.queue

            except Exception as e:
                app.logger.exception(e)

        if b_form.rim_field.data != session['wheel']['rim_id']:
            try:
                rim = db.session.query(Rims).filter_by(id=b_form.rim_field.data).first()
                session['wheel']['rim_id'] = rim.id
                session['rim'] = rim.as_dict()

                mru = Mru(session['rim_mru'])
                mru.add(rim.mru_props)
                session['rim_mru'] = mru.queue

            except Exception as e:
                app.logger.error(e)

        session['wheel']['spokes'] = b_form.spoke_field.data
        session['wheel']['pattern'] = b_form.pattern_field.data
        session['wheel']['nipple_length'] = b_form.nipple_length_field.data
        session.modified = True

    else:
        for e in b_form.errors.items():
            app.logger.error(e)

    if 'hub' in session and 'rim' in session:
        session['lengths'] = spoke_lengths(session['wheel'], session['hub'], session['rim'])

    app.logger.info(session)
    return redirect(url_for('index'))


@app.route('/wheel/add_rim/<int:rim_id>')
def wheel_add_rim(rim_id=None):
    try:
        rim = db.session.query(Rims).filter_by(id=rim_id).first()
        session['wheel']['rim_id'] = rim.id
        session['rim'] = rim.as_dict()

        mru = Mru(session['rim_mru'])
        mru.add(rim.mru_props)
        session['rim_mru'] = mru.queue

    except Exception as e:
        app.logger.error(e)

    if 'hub' in session and 'rim' in session:
        session['lengths'] = spoke_lengths(session['wheel'], session['hub'], session['rim'])

    app.logger.info(session)

    return redirect(url_for('rims_list'))


@app.route('/wheel/add_hub/<int:hub_id>')
def wheel_add_hub(hub_id=None):
    try:
        hub = db.session.query(Hubs).filter_by(id=hub_id).first()
        session['wheel']['hub_id'] = hub.id
        session['hub'] = hub.as_dict()

        mru = Mru(session['hub_mru'])
        mru.add(hub.mru_props)
        session['hub_mru'] = mru.queue

        session.modified = True

    except Exception as e:
        app.logger.error(e)

    if 'hub' in session and 'rim' in session:
        session['lengths'] = spoke_lengths(session['wheel'], session['hub'], session['rim'])

    app.logger.info(session)

    return redirect(url_for('hubs_list'))


@app.route('/rims/list')
@app.route('/rims/list/<int:page>')
def rims_list(page=1):
    g.bform = bform()
    g.sform = SearchForm(request.args)

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

    return render_template('rims.html.j2',
                           rims_paginated=rims,
                           form=form)


@app.route('/hubs/list')
@app.route('/hubs/list/<int:page>')
def hubs_list(page=1):
    app.logger.info(session)

    g.bform = bform()
    g.sform = SearchForm(request.args)

    hubs = db.session.query(Hubs)

    form = SearchForm(request.args)
    if form.validate():

        forr = form.forr.data
        search = form.search.data

        if forr:
            hubs = hubs.filter(Hubs.forr == forr)

        if search:
            hubs = hubs.filter(Hubs.description.like(f"%{search}%"))

    else:
        for e in form.errors.items():
            app.logger.error(e)

    hubs = hubs.order_by(Hubs.description.asc()).paginate(page=page, per_page=ITEMS_PER_PAGE)

    return render_template('hubs.html.j2',
                           hubs_paginated=hubs,
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404


if __name__ == '__main__':
    app.run()
