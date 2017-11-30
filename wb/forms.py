from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length, Regexp


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    forr = StringField(validators=[Length(max=1), Regexp(r'[FR]?')], default=None)
    size = IntegerField(default=None)
    search = StringField(default=None)
