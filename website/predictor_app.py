import flask
from flask import request
#from predictor_api import make_prediction

# Initialize the app

app = flask.Flask(__name__)

# An example of routing:
# If they go to the page "/" (this means a GET request
# to the page http://127.0.0.1:5000/)

@app.route("/", methods=["GET", "POST"])

def predict ():
    """
    request.args contains all the arguments passed by our form
    comes built in with flask.  It is a dictionary of the form 
    'form name (as set in templat)' (key): 'string in the textbox' (value)
    """
    print(request.args)
    if(request.args):
        x_input, predictions = make_prediction(request.args[['HomeGame', 'TeamScore', 'OppScore', 'Quarter', 'Time', 'Side', 'YardLine', 'Down', 'Distance']])
        print(x_input)
        return flask.render_template('predictor.html',
                                      inputs=x_input,
                                      prediction=predictions)
    else:
        """ for first load, requst.args will be an empty ImmutableDict
        type.  If this is the case we need to pass an empty string 
        into make_prediction function so no errors are thrown."""

        x_input, predictions = make_prediction({'HomeGame': 1, 'TeamScore': 0, 'OppScore':0 , 'Quarter':1, 'Time': "15:00", 'Side': 50, 'YardLine': 25, 'Down': 1, 'Distance': 10})
        return flask.render_template('predictor.html',
                                      inputs = x_input,
                                      prediction = predictions)
                                      
    if __name__=="__main__":
        # For local development, set to True:
        app.run(debug=False)
        # For publisc web serving:
        # app.run(host='0.0.0.0')
        app.run()


        
#['HomeGame', 'TeamScore', 'OppScore', 'Quarter', 'Time', 'Side', 'YardLine', 'Down', 'Distance']