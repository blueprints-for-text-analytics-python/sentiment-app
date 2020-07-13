import pickle
from flasgger import Swagger
from flask import Flask, request, jsonify
import preprocessing

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/v1/sentiment', methods=['POST'])
def predict():
  """API Endpoint used for serving the prediction function of the Sentiment Analysis model

  The sentiment analysis model has been trained using Amazon customer reviews and works best in similar scenarios
  When the text of a customer review is passed, it is cleaned and either a POSITIVE or NEGATIVE sentiment prediction is returned

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

def run_app():
  try:
    global saved_model, tfidf_vectorizer
    saved_model = pickle.load(open('models/sentiment_classification.pickle', 'rb'))
    tfidf_vectorizer = pickle.load(open('models/tfidf_vectorizer.pickle', 'rb'))
    print('model loaded')
  except Exception as e:
    raise ValueError('No model here')
  return app
