import flask

from decision_logic import home_page, wtcal_compute, wtcal_import


application = flask.Flask(__name__)


@application.context_processor
def utility_processor():
    def convert_name(name):
        new_name = ' '.join(name.split('_')).title()
        return new_name
    return dict(convert_name=convert_name)


@application.route('/', methods=['GET'])
def home():
    return home_page(flask)


@application.route('/wtcal', methods=['GET', 'POST'])
def wtcal():
    return wtcal_compute(flask)

if __name__ == '__main__':
    application.run(debug=True)
