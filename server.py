#!flask/bin/python
from flask import Flask, jsonify, request
from datetime import datetime
from sklearn.externals import joblib
import pyowm
import project_commons


app = Flask(__name__, static_url_path='')
hypothesis = joblib.load("%s" % project_commons.CLASSIFIER_PKL)
weather_api = pyowm.OWM(project_commons.OPEN_WEATHER_API_KEY)
label_encoder = joblib.load("%s" % project_commons.PRIMARY_TYPE_LABEL_ENCODER_PKL)


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/predict', methods=['GET'])
def predict():
    query_arguments = request.args.to_dict()

    lat = query_arguments["lat"]
    lon = query_arguments["lon"]
    current_day_of_year = datetime.now().strftime(project_commons.DATE_LEARNING_FORMAT)

    current_weather = weather_api.weather_at_coords(float(lat), float(lon)).get_weather().get_temperature("celsius").get("temp")

    result_value = hypothesis.predict([[current_weather, lat, lon, current_day_of_year]])
    result_crime = label_encoder.inverse_transform(result_value)[0]
    return jsonify(result_crime)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
