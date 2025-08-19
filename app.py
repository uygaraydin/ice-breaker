# Import Flask components for web application
from flask import Flask, render_template, request, jsonify
# Import dotenv to load environment variables
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom ice_break_with function
from ice_breaker import ice_break_with


# Create Flask application instance
app = Flask(__name__)


# Define route for the home page
@app.route("/")
def index():
    # Render and return the index.html template
    return render_template("index.html")


# Define route for processing POST requests
@app.route("/process", methods=["POST"])
def process():
    # Get the name from the form data sent in the POST request
    name = request.form["name"]
    # Call ice_break_with function to get summary and profile picture URL
    summary,profile_pic_url = ice_break_with(
        name=name
    )
    # Return JSON response with summary data and photo URL
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "photoUrl": profile_pic_url,
        }
    )

# Main execution block (only runs when script is executed directly)
if __name__ == "__main__":
    # Run the Flask application on port 5001
    app.run(port=5001)