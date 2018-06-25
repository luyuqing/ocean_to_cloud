from flask import Flask, render_template, request, jsonify
from math import ceil
from werkzeug.datastructures import MultiDict

from prepare import zip_form
from model import GeometryInput, MaterialInput, \
                  LoadInput, SafetyClass, Other, \
                  CalWith, ImportFrom
from compute import cal_pressure_containment, cal_collaps, \
                    cal_prop_buckling, cal_reeling


application = Flask(__name__)


@application.context_processor
def utility_processor():
    def convert_name(name):
        new = ' '.join(name.split('_')).title()
        return new
    return dict(convert_name=convert_name)


@application.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@application.route('/wtcal', methods=['GET', 'POST'])
def index():

    import_from = list(ImportFrom(request.form))[0]
    import_submit = list(ImportFrom(request.form))[1]

    # m = MultiDict([('steel_diameter', 5.0),
    #                ('corrosion_allowance', 5.0)])
    # geo = GeometryInput(m)
    # geo_fields = zip_form(geo)

    geo = GeometryInput(request.form)
    geo_fields = zip_form(geo)

    material = MaterialInput(request.form)
    material_fields = zip_form(material)

    load = LoadInput(request.form)
    load_fields = zip_form(load)

    safety = SafetyClass(request.form)
    safety_fields = zip_form(safety)

    other = Other(request.form)
    other_fields = zip_form(other)

    cal_with_fields = CalWith(request.form)

    if request.method == 'POST':
        if geo.validate() and material.validate() and \
           load.validate() and safety.validate():
            steel_diameter = geo.steel_diameter.data
            corrosion_allowance = geo.corrosion_allowance.data

            fabrication_method = material.fabrication_method.data
            pipe_material = material.pipe_material.data
            max_design_temperature = material.max_design_temperature.data
            supplimentary_d_fulfilled = material.supplimentary_d_fulfilled.data
            supplimentary_u_fulfilled = material.supplimentary_u_fulfilled.data
            any_inner_metal_layer = material.any_inner_metal_layer.data
            cladded_or_lined = material.cladded_or_lined.data
            metal_layer_type = material.metal_layer_type.data

            design_pressure = load.design_pressure.data
            level = load.level.data
            max_contents_density = load.max_contents_density.data
            water_depth_for_bursting = load.water_depth_for_bursting.data
            water_depth_for_collapse_and_prop_buckling = load.water_depth_for_collapse_and_prop_buckling.data
            sea_water_density = load.sea_water_density.data

            contents_type = safety.contents_type.data
            operation_zone = safety.operation_zone.data

            # Example
            example_param_float = other.example_param_float.data
            example_param_select = other.example_param_select.data

            pressure_containment = cal_with_fields.pressure_containment.data
            collaps = cal_with_fields.collaps.data
            propgation_buckling = cal_with_fields.propgation_buckling.data
            reeling_screening_check = cal_with_fields.reeling_screening_check.data
            vessel = cal_with_fields.vessel.data

            res = dict()
            p1, p2, p3, p4 = 0, 0, 0, 0
            
            if pressure_containment is True:
                p1 = cal_pressure_containment(steel_diameter,
                                              corrosion_allowance,
                                              fabrication_method,
                                              pipe_material,
                                              max_design_temperature,
                                              supplimentary_d_fulfilled,
                                              supplimentary_u_fulfilled,
                                              design_pressure,
                                              level,
                                              max_contents_density,
                                              sea_water_density,
                                              water_depth_for_bursting,
                                              contents_type,
                                              operation_zone)
            if collaps is True:
                p2 = cal_collaps(steel_diameter,
                                 corrosion_allowance,
                                 fabrication_method,
                                 pipe_material,
                                 max_design_temperature,
                                 supplimentary_d_fulfilled,
                                 supplimentary_u_fulfilled,
                                 sea_water_density,
                                 water_depth_for_collapse_and_prop_buckling,
                                 contents_type,
                                 operation_zone)
            if propgation_buckling is True:
                p3 = cal_prop_buckling(steel_diameter,
                                       corrosion_allowance,
                                       fabrication_method,
                                       pipe_material,
                                       max_design_temperature,
                                       supplimentary_d_fulfilled,
                                       supplimentary_u_fulfilled,
                                       sea_water_density,
                                       water_depth_for_collapse_and_prop_buckling,
                                       contents_type,
                                       operation_zone)
            if reeling_screening_check is True:
                p4 = cal_reeling(steel_diameter,
                                 fabrication_method,
                                 vessel,
                                 any_inner_metal_layer,
                                 cladded_or_lined)
            # print(p1, p2, p3, p4)
            res['p0'] = ''
            res['p1'] = p1 if p1 else ''
            res['p2'] = p2 if p2 else ''
            res['p3'] = p3 if p3 else ''
            res['p4'] = p4 if p4 else ''

            # to cal max wt, all p1-p4 must be float not string
            wt_cal = True
            for k, v in res.items():
                if not isinstance(v, float) and v != '':
                    wt_cal = False
                    break
            if wt_cal is True:
                max_ = max(p1, p2, p3, p4)
                res['p0'] = ceil(max_*100)/100

            # print(res)

            str_candidates = {'p0': 'Min Requirement For Wall Thickness',
                              'p1': 'Min Requirement For Pressure Containment',
                              'p2': 'Min Requirement For Collaps',
                              'p3': 'Min Requirement For Propgation Buckling',
                              'p4': 'Min Requirement For Reeling Screening Check'}
            string_to_p = {v: k for k, v in str_candidates.items()} 
            # From string components if value is not ''
            final_strings = [str_candidates[p] for p in res if res[p]]
            # print(final_strings, string_to_p)
            valid_string = []
            p_values = list()
            for s in final_strings:
                valid_string.append(s)
                p_values.append(res[string_to_p[s]])
            zip_results = list(zip(valid_string, p_values))
            # print(zip_results)
            result = ''
            for v in zip_results:
                result = result + v[0] + ': ...' + '{:.2f}'.format(v[1]) + '\n'
            # print(result)
            return jsonify({"result": result})
        # else:
        #     m = MultiDict([('steel_diameter', 5.0),
        #                    ('corrosion_allowance', 5.0)])
        #     geo = GeometryInput(m)
        else:
            return jsonify({"result": "Please Fill In Blanks With Valid Values."})

    return render_template("view.html",
                           import_from=import_from,
                           import_submit=import_submit,
                           geo_fields=geo_fields,
                           material_fields=material_fields,
                           load_fields=load_fields,
                           safety_fields=safety_fields,
                           other_fields=other_fields,
                           cal_with_fields=cal_with_fields)


if __name__ == '__main__':
    application.run(debug=True)
