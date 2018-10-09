from flask import Flask, render_template, Response, redirect, request, jsonify
from flask_restful import Resource, Api
from produce_output import output_class_builder 

app = Flask(__name__)
api = Api(app)




@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html', flask_message = 'flask is great')

output_class = output_class_builder()
output_class.output_threading()

@app.route('/window_flask')
def window_flask():
    global output_class
    return jsonify({'x':output_class.x, 'y':output_class.y})



class window_rest(Resource):
    def get(self):
        global output_class
        return jsonify({'x':output_class.x, 'y':output_class.y})

api.add_resource(window_rest, '/window_rest')



if __name__ == '__main__':
    app.run(debug=True)