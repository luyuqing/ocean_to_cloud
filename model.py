from wtforms import Form, FloatField, validators

class InputForm(Form):
    total_length = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    single_length = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    welding_coverage = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    default_spacing = FloatField(label='(m)',
                    validators=[validators.InputRequired()])