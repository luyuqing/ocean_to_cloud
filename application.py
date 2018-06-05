from flask import Flask, render_template, request
from model import InputForm
from compute import compute

def zip_form(form):
    list_1 = []
    list_2 = []
    table_list = []
    for field in form:
        table_list.append(field)
    for i, v in enumerate(table_list):
        print(i, v)
        if i % 2 == 0:
            list_1.append(v)
        else:
            list_2.append(v)           
    return list(zip(list_1, list_2))

application = Flask(__name__)
@application.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    final = zip_form(form)
    result = ''
    if request.method == 'POST' and form.validate():
        total_length = form.total_length.data
        single_length = form.single_length.data
        welding_coverage = form.welding_coverage.data
        default_spacing = form.default_spacing.data

        result = compute(total_length, single_length, welding_coverage, default_spacing)

    return render_template("view.html", final=final, result=result)

if __name__ == '__main__':
    application.run(debug=True)