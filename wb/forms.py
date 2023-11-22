from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired, Optional, Email

from wb.models import nipple_corrections, patterns, rim_sizes, spoke_counts


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

    hub_field = SelectField('Previously Selected Hubs', choices=[], validators=[Optional()], coerce=int)
    rim_field = SelectField('Previously Selected Rims', choices=[], validators=[Optional()], coerce=int)
    spoke_field = SelectField('Spokes', choices=spoke_counts, coerce=int)
    pattern_field = SelectField('Pattern', choices=patterns, coerce=int)
    nipple_length_field = SelectField('Nipple Length', choices=nipple_corrections, coerce=int)


class HubForm(FlaskForm):
    description = StringField("Description", description="Include maker and model and whether or not it's a disc hub",
                              validators=[InputRequired()])
    s = FloatField("S", description="Spoke hole diameter", default=2.5)
    dl = FloatField("DL", description="Flange diameter measured center to center of the spoke holes")
    dr = FloatField("DR", description="")
    wl = FloatField("WL",
                    description="Distance between the center of the hub between the locknuts and the center of the flange")
    wr = FloatField("WR", description="")
    old = FloatField("OLD", description="Over Locknut Distance or the distance between the locknuts")
    forr = SelectField("Front or Rear", choices=[('F', 'Front'), ('R', 'Rear')])
    comment = StringField("Comment")
    email = EmailField("Email", validators=[Email()],
                       description="Used to contact you if there's a problem with your entry. It's not displayed anywhere on the site.")


class RimForm(FlaskForm):
    description = StringField("Description", description="Include the maker and model if possible",
                              validators=[InputRequired()])
    size = SelectField('Rim Size', choices=rim_sizes, coerce=int)
    erd = FloatField("ERD", description="Effective Rim Diameter")
    osb = FloatField("OSB", description="Offset Spoke Bed", default=0.0)
    comment = StringField("Comment")
    email = EmailField("Email", validators=[Email()],
                       description="Used to contact you if there's a problem with your entry. It's not displayed anywhere on the site.")

