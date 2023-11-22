import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from wb.forms import BuilderForm, HubForm, RimForm, SearchForm
from wb.models import Hubs, Mru, Rims, Wheel, metadata, spoke_lengths, nipple_size_for_display

app = Flask(__name__)
FORMAT = "%(asctime)-15s [%(filename)s:%(lineno)s : %(funcName)s()] %(message)s"
formatter = logging.Formatter(FORMAT)

# initialize the log handler
logHandler = TimedRotatingFileHandler('logs/app.log', when='D', backupCount=7)
logHandler.setFormatter(formatter)

# set the app logger level
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logHandler)
app.logger.info("Starting up...")

config = os.environ.get('WB_CONFIG', 'config.DevelopmentConfig')
app.config.from_object(config)

if app.config['SENTRY_DSN']:
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0
    )

db = SQLAlchemy(metadata=metadata)
db.init_app(app)

ITEMS_PER_PAGE = 15


def bform(data=None):
    # app.logger.info(session)

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

    if 'lengths' not in session:
        session['lengths'] = (0, 0)


@app.route('/')
def index():
    g.bform = bform()
    return render_template('index.html.j2', show_builder=True)


@app.route('/wheel', methods=["POST"])
def wheel():
    # app.logger.info(session)

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
        session['wheel']['nipple_length_for_display'] = nipple_size_for_display(b_form.nipple_length_field.data)
        session.modified = True

    else:
        for e in b_form.errors.items():
            app.logger.error(e)

    if 'hub' in session and 'rim' in session:
        session['lengths'] = spoke_lengths(session['wheel'], session['hub'], session['rim'])

    # app.logger.info(session)
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

    # app.logger.info(session)

    return redirect(url_for('index'))


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

    # app.logger.info(session)

    return redirect(url_for('index'))


@app.route('/wheel_print')
def wheel_print():
    rim = db.session.query(Rims).filter_by(id=session['wheel']['rim_id']).first()
    hub = db.session.query(Hubs).filter_by(id=session['wheel']['hub_id']).first()

    return render_template('print.html.j2',
                           show_builder=False,
                           hub=hub,
                           rim=rim,
                           wheel=session['wheel'])


@app.route('/rims/add', methods=["GET", "POST"])
def rims_add():
    form = RimForm(request.form)

    if request.method == "POST" and form.validate_on_submit():

        rim = Rims()
        form.populate_obj(rim)
        db.session.add(rim)
        db.session.commit()

        flash("Rim Created")

        if app.config.get('MAIL_SERVER', None):
            mail = Mail(app)
            body = render_template('rims_email.txt.j2', form=form, rim=rim)

            msg = Message(subject="New Rim submitted",
                          body=body,
                          recipients=[app.config.get('MAIL_TO', None)])
            try:
                mail.send(msg)
            except Exception as e:
                app.logger.error(e)

        return redirect(url_for("wheel_add_rim", rim_id=rim.id))

    else:
        for e in form.errors.items():
            flash(f"{e[0]} - {e[1][0]}")

    return render_template('rims_add.html.j2',
                           form=form)


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
                           form=form,
                           show_builder=True)


@app.route('/hubs/add', methods=["GET", "POST"])
def hubs_add():
    form = HubForm(request.form)

    if request.method == "POST" and form.validate_on_submit():

        hub = Hubs()
        form.populate_obj(hub)
        db.session.add(hub)
        db.session.commit()

        flash("Hub Created")

        if app.config.get('MAIL_SERVER', None):
            mail = Mail(app)

            body = render_template('hubs_email.txt.j2', form=form, hub=hub)

            msg = Message(subject="New Hub submitted",
                          body=body,
                          sender="hello@jmoore.me",
                          recipients=[app.config.get('MAIL_TO', None)])
            try:
                mail.send(msg)
            except Exception as e:
                app.logger.error(e)

        return redirect(url_for("wheel_add_hub", hub_id=hub.id))

    else:
        for e in form.errors.items():
            flash(f"{e[0]} - {e[1][0]}")

    return render_template('hubs_add.html.j2',
                           form=form)


@app.route('/hubs/list')
@app.route('/hubs/list/<int:page>')
def hubs_list(page=1):
    # app.logger.info(session)

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
                           form=form,
                           show_builder=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2'), 404


if __name__ == '__main__':
    app.run()
