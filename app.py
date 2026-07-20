from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def home():

    quote = ""

    if request.method == "POST":

        mood = request.form["mood"]

        prompt = f"""
Generate one short motivational quote for someone who is feeling {mood}.

Rules:
- Maximum 20 words.
- Positive and inspiring.
- Do not use quotation marks.
"""

        try:
            response = client.models.generate_content(
                 model="gemini-flash-lite-latest",
                 contents=prompt
             )
            

            quote = response.text

        except Exception as e:
            quote = f"Error: {e}"

    return render_template("index.html", quote=quote)


if __name__ == "__main__":
    app.run(debug=True)