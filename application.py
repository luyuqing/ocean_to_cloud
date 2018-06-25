from flask import Flask

from decision_logic import home_page, wtcal_compute


application = Flask(__name__)


@application.context_processor
def utility_processor():
    def convert_name(name):
        new = ' '.join(name.split('_')).title()
        return new
    return dict(convert_name=convert_name)


@application.route('/', methods=['GET'])
def home():
    return home_page()


@application.route('/wtcal', methods=['GET', 'POST'])
def wtcal():
    return wtcal_compute()

if __name__ == '__main__':
    application.run(debug=True)
