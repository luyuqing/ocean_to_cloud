from werkzeug.datastructures import MultiDict

from prepare import zip_form, wtcal_output
from model import GeometryInput, MaterialInput, MetalLayer, LoadInput, \
    SafetyClass, Other, CalWith, ImportFrom
from compute import cal_pressure_containment, cal_collaps, \
    cal_prop_buckling, cal_reeling


def home_page(flask):
    return flask.render_template("home.html")


def wtcal_import():
    # m = MultiDict([('steel_outer_diameter', 5.0),
    #                 ('corrosion_allowance', 5.0)])
    # geo = GeometryInput(m)
    # geo_fields = zip_form(geo)
    geo = GeometryInput(flask.request.form)
    geo_fields = zip_form(geo)

    import_ = ImportFrom()
    import_from = list(import_)[0]

    if request.method == 'POST':
        res = {"steel_diameter": 5, "corrosion_allowance": 5}
        return jsonify(res)
    return render_template("wtcal.html",
                           import_from=import_from,
                           import_submit=import_submit,
                           geo_fields=geo_fields)


def wtcal_compute(flask):
    geo = GeometryInput(flask.request.form)
    geo_fields = zip_form(geo)

    material = MaterialInput(flask.request.form)
    material_fields = zip_form(material)

    metal = MetalLayer(flask.request.form)
    metal_fields = zip_form(metal)

    load = LoadInput(flask.request.form)
    load_fields = zip_form(load)

    safety = SafetyClass(flask.request.form)
    safety_fields = zip_form(safety)

    other = Other(flask.request.form)
    other_fields = zip_form(other)

    cal_with_fields = CalWith(flask.request.form)

    if flask.request.method == 'POST':
        if geo.validate() and material.validate() and \
           load.validate() and safety.validate():
            steel_outer_diameter = geo.steel_outer_diameter.data
            corrosion_allowance = geo.corrosion_allowance.data

            fabrication_method = material.fabrication_method.data
            pipe_material = material.pipe_material.data
            max_design_temperature = material.max_design_temperature.data
            supplimentary_d_fulfilled = material.supplimentary_d_fulfilled.data
            supplimentary_u_fulfilled = material.supplimentary_u_fulfilled.data

            any_inner_metal_layer = metal.any_inner_metal_layer.data
            cladded_or_lined = metal.cladded_or_lined.data
            metal_layer_type = metal.metal_layer_type.data

            design_pressure = load.design_pressure.data
            level = load.level.data
            max_contents_density = load.max_contents_density.data
            water_depth_for_bursting = load.water_depth_for_bursting.data
            water_depth_for_collapse_and_prop_buckling = load.water_depth_for_collapse_and_prop_buckling.data
            sea_water_density = load.sea_water_density.data

            contents_type = safety.contents_type.data
            operation_zone = safety.operation_zone.data

            # Example Other
            example_param_float = other.example_param_float.data
            example_param_select = other.example_param_select.data

            pressure_containment = cal_with_fields.pressure_containment.data
            collaps = cal_with_fields.collaps.data
            propgation_buckling = cal_with_fields.propgation_buckling.data
            reeling_screening_check = cal_with_fields.reeling_screening_check.data
            vessel = cal_with_fields.vessel.data

            r1, r2, r3, r4 = 0, 0, 0, 0

            if pressure_containment is True:
                r1 = cal_pressure_containment(steel_outer_diameter,
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
                r2 = cal_collaps(steel_outer_diameter,
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
                r3 = cal_prop_buckling(steel_outer_diameter,
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
                r4 = cal_reeling(steel_outer_diameter,
                                 fabrication_method,
                                 vessel,
                                 any_inner_metal_layer,
                                 cladded_or_lined)

            result = wtcal_output(r1=r1, r2=r2, r3=r3, r4=r4)
            return flask.jsonify({"result": result})
        else:
            return flask.jsonify({"result": "Please Fill In Blanks With Valid Values."})

    return flask.render_template("wtcal.html",
                                 geo_fields=geo_fields,
                                 material_fields=material_fields,
                                 metal_fields=metal_fields,
                                 load_fields=load_fields,
                                 safety_fields=safety_fields,
                                 other_fields=other_fields,
                                 cal_with_fields=cal_with_fields)
