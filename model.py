from wtforms import Form, FloatField, SelectField, \
    BooleanField, SubmitField, validators


class ImportFrom(Form):
    import_from = SelectField(choices=[('', ''),
                                       ('module1', 'module1'),
                                       ('module2', 'module2')])
    submit_import = SubmitField('Import')


class GeometryInput(Form):
    steel_diameter = FloatField(label='mm',
                                validators=[validators.InputRequired()])
    corrosion_allowance = FloatField(label='(mm)',
                                     validators=[validators.InputRequired()])


class MaterialInput(Form):
    fabrication_method = SelectField(label='', choices=[('HFW', 'HFW'),
                                                        ('SMLS', 'SMLS'),
                                                        ('MWP', 'MWP')])
    pipe_material = SelectField(label='', choices=[('DNV360', 'DNV360'),
                                                   ('DNV415', 'DNV415'),
                                                   ('DNV450', 'DNV450'),
                                                   ('DNV22Cr', 'DNV22Cr'),
                                                   ('DNV25Cr', 'DNV25Cr')])
    max_design_temperature = FloatField(label='(°C)',
                                        validators=[validators.InputRequired()])
    supplimentary_d_fulfilled = SelectField(label='', choices=[('yes', 'YES'),
                                                               ('no', 'NO')])
    supplimentary_u_fulfilled = SelectField(label='', choices=[('yes', 'YES'),
                                                               ('no', 'NO')])
    any_inner_metal_layer = SelectField(label='', choices=[('yes', 'YES'),
                                                           ('no', 'NO')])
    cladded_or_lined = SelectField(label='', choices=[('Cladded', 'Cladded'),
                                                      ('Lined', 'Lined')])
    metal_layer_type = SelectField(label='', choices=[('UNS31603', 'UNS31603'),
                                                      ('UNSN06625', 'UNSN06625')])


class LoadInput(Form):
    design_pressure = FloatField(label='[Barg]',
                                 validators=[validators.InputRequired()])
    level = FloatField(label='(m)',
                       validators=[validators.InputRequired()])
    max_contents_density = FloatField(label='(kg/m3)',
                                      validators=[validators.InputRequired()])
    water_depth_for_bursting = FloatField(label='(m)',
                                          validators=[validators.InputRequired()])
    water_depth_for_collapse_and_prop_buckling = FloatField(label='(m)',
                                                            validators=[validators.InputRequired()])
    sea_water_density = FloatField(label='(kg/m3)',
                                   validators=[validators.InputRequired()])


class SafetyClass(Form):
    contents_type = SelectField(label='', choices=[('Non-flammable', 'Non-flammable'),
                                                   ('Flammable', 'Flammable')])
    operation_zone = SelectField(label='', choices=[('Zone2', 'Zone2'),
                                                    ('Zone1', 'Zone1'),
                                                    ('Both', 'Both')])


class Other(Form):
    example_param_float = FloatField(label='(m)',
                                     validators=[validators.InputRequired()])
    example_param_select = SelectField(label='', choices=[('Choice1', 'Choice1'),
                                                          ('Choice2', 'Choice2'),
                                                          ('Choice3', 'Choice3')])


class CalWith(Form):
    pressure_containment = BooleanField(label='')
    collaps = BooleanField(label='')
    propgation_buckling = BooleanField(label='')
    reeling_screening_check = BooleanField(label='')
    vessel = SelectField(label='', choices=[('7Oceans', '7Oceans'),
                                            ('7Navica', '7Navica')])
