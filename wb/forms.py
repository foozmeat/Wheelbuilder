from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Optional

from wb.models import patterns, nipple_corrections, spoke_counts, rim_sizes


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    forr = SelectField('Front or Rear', choices=[("", "Front or Rear"), ("F", "Front"), ("R", "Rear")], default="",
                       validators=[Optional()])
    size = SelectField('Rim Size', choices=[(0, "Any Size")] + rim_sizes, coerce=int, validators=[Optional()])
    search = StringField(default=None)


class BuilderForm(FlaskForm):
    class Meta:
        csrf = False

    hub_field = SelectField('Hub Selector', choices=[], validators=[Optional()], coerce=int)
    rim_field = SelectField('Rim Selector', choices=[], validators=[Optional()], coerce=int)
    spoke_field = SelectField('Spokes', choices=spoke_counts, coerce=int)
    pattern_field = SelectField('Pattern', choices=patterns, coerce=int)
    nipple_length_field = SelectField('Nipple Length', choices=nipple_corrections, coerce=int)
