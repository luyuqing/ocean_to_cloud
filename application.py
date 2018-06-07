from flask import Flask, render_template, request, jsonify

from prepare import zip_form
from compute import compute
from model import GeometryInput, MaterialInput, \
                  LoadInput, SafetyClass, CalWith


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
            max_contents_density_at_operation = load.max_contents_density_at_operation.data
            water_depth_for_bursting = load.water_depth_for_bursting.data
            water_depth_for_collapse_and_prop_buckling = load.water_depth_for_collapse_and_prop_buckling.data
            sea_water_density = load.sea_water_density.data

            contents_type = safety.contents_type.data
            operation_zone = safety.operation_zone.data

            pressure_containment = cal_with_fields.pressure_containment.data
            collaps = cal_with_fields.collaps.data
            propgation_buckling = cal_with_fields.propgation_buckling.data
            reeling_screening_check = cal_with_fields.reeling_screening_check.data
            vessel_if_reeling_check_is_requried = cal_with_fields.vessel_if_reeling_check_is_requried.data

            return jsonify({"result": (str(steel_diameter) + '\n' + str(collaps))})
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
