from wtforms import Form, FloatField, SelectField, BooleanField, validators

class InputForm(Form):
    total_length = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    single_length = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    welding_coverage = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    default_spacing = FloatField(label='(m)',
                    validators=[validators.InputRequired()])
    checked = SelectField(label='', choices=[('yes', 'YES'), ('no', 'NO')])
    language = SelectField(label='', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])