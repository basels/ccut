from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TransformationForm(FlaskForm):
    in_unit  = StringField('Input Unit',  validators=[DataRequired()])
    out_unit = StringField('Output Unit', validators=[DataRequired()])
    in_val   = StringField('Input Value', validators=[DataRequired()])
    submit   = SubmitField('Generate')