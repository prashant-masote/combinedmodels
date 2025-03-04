import warnings
# Refine warning filter to suppress InconsistentVersionWarning from scikit-learn
warnings.filterwarnings('ignore', category=UserWarning, message='.*InconsistentVersionWarning.*')

from flask import Flask, request, render_template
import numpy as np
import pickle

# Load the models and preprocessors
crop_model = pickle.load(open("model.pkl", "rb"))  # Replace with your crop model file
production_model = pickle.load(open("dtr.pkl", "rb"))  # Replace with your production model file
production_preprocessor = pickle.load(open("preprocessor.pkl", "rb"))  # Replace with your preprocessor file

# Initialize Flask app
app = Flask(__name__)

# Define valid ranges for crop prediction inputs
VALID_RANGES = {
    "Nitrogen": (0, 140),
    "Phosphorus": (5, 145),
    "Potassium": (5, 205),
    "temperature": (8.83, 43.68),
    "humidity": (14.26, 99.98),
    "pH": (3.50, 9.94),
    "rainfall": (20.21, 298.56),
}

def validate_input(input_data, valid_ranges):
    """
    Validate input values against predefined ranges.
    """
    for key, value in zip(valid_ranges.keys(), input_data):
        min_val, max_val = valid_ranges[key]
        if not (min_val <= value <= max_val):
            return f"{key} value {value} is out of range ({min_val}-{max_val})."
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict-crop", methods=["POST"])
def predict_crop():
    try:
        # Collect input data
        float_features = [float(x) for x in request.form.values()]
        input_data = np.array(float_features)

        # Validate input data
        validation_error = validate_input(float_features, VALID_RANGES)
        if validation_error:
            return render_template("index.html", prediction_text=f"Error: {validation_error}")

        # Make prediction
        prediction = crop_model.predict([input_data])
        predicted_crop = prediction[0] if isinstance(prediction, (list, np.ndarray)) else prediction

        return render_template("index.html", prediction_text=f"The Predicted Crop is: {predicted_crop}")
    except ValueError:
        return render_template("index.html", prediction_text="Error: Invalid input. Please enter valid numeric values.")
    except Exception as e:
        return render_template("index.html", prediction_text=f"An unexpected error occurred: {str(e)}")

@app.route("/predict-production", methods=["POST"])
def predict_production():
    try:
        # Collect input data
        features = [
            request.form["Year"],
            request.form["average_rain_fall_mm_per_year"],
            request.form["pesticides_tonnes"],
            request.form["avg_temp"],
            request.form["Area"],
            request.form["Item"],
        ]
        features_array = np.array([features], dtype=object)

        # Transform features using the preprocessor
        transformed_features = production_preprocessor.transform(features_array)

        # Make prediction
        prediction = production_model.predict(transformed_features)
        predicted_value = prediction[0] if isinstance(prediction, (list, np.ndarray)) else prediction

        return render_template("index.html", prediction_text=f"The Predicted Production is: {predicted_value}")
    except ValueError:
        return render_template("index.html", prediction_text="Error: Invalid input. Please enter valid values.")
    except Exception as e:
        return render_template("index.html", prediction_text=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
