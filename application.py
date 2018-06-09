from collections import OrderedDict
from flask import Flask, render_template, request, jsonify

from prepare import zip_form
from model import GeometryInput, MaterialInput, \
                  LoadInput, SafetyClass, CalWith
from compute import cal_pressure_containment, cal_collaps, \
                    cal_prop_buckling, cal_reeling


application = Flask(__name__)


@application.context_processor
def utility_processor():
    def convert_name(name):
        new = ' '.join(name.split('_')).title()
        return new
    return dict(convert_name=convert_name)


@application.route('/', methods=['GET', 'POST'])
def index():
    geo = GeometryInput(request.form)
    geo_fields = list(geo)
    geo_diameter_name = geo_fields[0].name
    geo_diameter_field = geo_fields[0]
    geo_diameter_unit = geo_fields[1]
    geo_corrosion_name = geo_fields[2].name
    geo_corrosion_field = geo_fields[2]
    geo_corrosion_label = geo_fields[2].label

    material = MaterialInput(request.form)
    material_fields = zip_form(material)

    load = LoadInput(request.form)
    load_fields = zip_form(load)

    safety = SafetyClass(request.form)
    safety_fields = zip_form(safety)

    cal_with_fields = CalWith(request.form)

    if request.method == 'POST':
        if geo.validate() and material.validate() and \
           load.validate() and safety.validate():
            steel_diameter_data = geo.steel_diameter_data.data
            steel_diameter_unit = geo.steel_diameter_unit.data
            if steel_diameter_unit == 'inch':
                steel_diameter = steel_diameter_data * 25.4
            else:
                steel_diameter = steel_diameter_data
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

            pressure_containment = cal_with_fields.pressure_containment.data
            collaps = cal_with_fields.collaps.data
            propgation_buckling = cal_with_fields.propgation_buckling.data
            reeling_screening_check = cal_with_fields.reeling_screening_check.data
            vessel = cal_with_fields.vessel.data

            res = OrderedDict()
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
                if not isinstance(v, float) and not k == 'p0':
                    wt_cal = False
                    break
            if wt_cal is True:
                max_ = max(p1, p2, p3, p4)
                res['p0'] = round(max_, 2)
                print(max_)

            # print(res)
            return jsonify({"result": "Min Requirement For Wall Thickness: ...{0}\n\
                                       Min Requirement For Pressure Containment: ...{1}\n\
                                       Min Requirement For Collaps: ...{2}\n\
                                       Min Requirement For Propgation Buckling: ...{3}\n\
                                       Min Requirement For Reeling Screening Check: ...{4}\n\
                                       ".format(res['p0'], res['p1'], res['p2'], res['p3'], res['p4'])})

        else:
            return jsonify({"result": "Please Fill In Blanks With Valid Values."})

    return render_template("view.html",
                           geo_diameter_name=geo_diameter_name,
                           geo_diameter_field=geo_diameter_field,
                           geo_diameter_unit=geo_diameter_unit,
                           geo_corrosion_name=geo_corrosion_name,
                           geo_corrosion_field=geo_corrosion_field,
                           geo_corrosion_label=geo_corrosion_label,
                           material_fields=material_fields,
                           load_fields=load_fields,
                           safety_fields=safety_fields,
                           cal_with_fields=cal_with_fields)


if __name__ == '__main__':
    application.run(debug=True)
