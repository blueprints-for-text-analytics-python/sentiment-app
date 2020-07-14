import pickle
from flasgger import Swagger
from flask import Flask, request, jsonify
import preprocessing

# Instantiating the Flask app
app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/v1/sentiment', methods=['POST'])
def predict():
  """API Endpoint used for serving the prediction function of the Sentiment Analysis model

  The sentiment analysis model has been trained using Amazon customer reviews and works best in similar scenarios
  When the text of a customer review is passed, it is cleaned and either a POSITIVE or NEGATIVE sentiment prediction is returned
  Change

  ---
  parameters:
    - in: body 
      name: body 
      schema:
        id: schema_id
        required:
          - review_text
        properties:
          review_text:
            type: string
	    description: Input review text that needs to be scored
	    default: "This is a great product. I would highly recommend it!"
  responses:
    200:
      description: SUCCESS
      examples: {"prediction":"POSITIVE"}
  """
  sentiment_label = ["NEGATIVE", "POSITIVE"]
  response = dict()
  if request.method == 'POST':
    data = request.get_json()
    text_clean = preprocessing.clean(data['review_text'])
    text_tfidf = tfidf_vectorizer.transform([text_clean])
    output = saved_model.predict(text_tfidf)
    response["prediction"] = sentiment_label[output.item()]
  return jsonify(response)

@app.route('/api/v1/classifybugs', methods=['POST'])
def bugs_classification():
  """API Endpoint used for serving the classification function of the Bugs Analysis model

  The classifier was trained using the JDT bugs dataset from BugZilla 
  When the text of a bug report is passed, it is cleaned and one of the five identified categories are returned APT, Core, Debug, Doc, Text, UI

  ---
  parameters:
    - in: body 
      name: body 
      schema:
        id: schema_id
        required:
          - bug_report
        properties:
          bug_report:
            type: string
            description: Text from the bug report that is to be classified
            default: "I tried to build and deploy this script but got a ResourceNotFoundException"
  responses:
    200:
      description: SUCCESS
      examples: {"prediction":"CORE"}
  """
  bugs_label = ["APT", "Core", "Debug", "Doc", "Text", "UI"]
  response = dict()
  if request.method == 'POST':
    data = request.get_json()
    text_clean = preprocessing.clean(data['review_text'])
    text_tfidf = tfidf_vectorizer_bugs.transform([text_clean])
    output = bugs_classifier.predict(text_tfidf)
    response["prediction"] = output.item()
  return jsonify(response)


def run_app():
  try:
    global saved_model, tfidf_vectorizer
    saved_model = pickle.load(open('models/sentiment_classification.pickle', 'rb'))
    tfidf_vectorizer = pickle.load(open('models/tfidf_vectorizer.pickle', 'rb'))
    print('sentiment models loaded')
    global bugs_classifier, tfidf_vectorizer_bugs
    bugs_classifier = pickle.load(open('models/bugs_classifier.pickle', 'rb'))
    tfidf_vectorizer_bugs = pickle.load(open('models/tfidf_vectorizer_bugs.pickle', 'rb'))
    print('bugs classification models loaded')
  except Exception as e:
    raise ValueError('No model here')
  return app
