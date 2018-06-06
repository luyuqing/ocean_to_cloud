from flask import Flask, render_template, request

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




    # final = zip_form(form)
    # result = ''
    # if request.method == 'POST' and form.validate():
    #     total_length = form.total_length.data
    #     single_length = form.single_length.data
    #     welding_coverage = form.welding_coverage.data
    #     default_spacing = form.default_spacing.data
    #     c = form.checked.data
    #     print(c)

    #     result = compute(total_length, single_length, welding_coverage, default_spacing)

    # return render_template("view.html", final=final, result=result)

if __name__ == '__main__':
    application.run(debug=True)
