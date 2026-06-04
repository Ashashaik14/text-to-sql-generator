from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_sql(user_input):
    prompt = f"""
You are an expert SQL Query Generator.

Convert the user's natural language request into a valid SQL query.

Rules:
- Return ONLY the SQL query.
- Do NOT provide explanations.
- Do NOT use markdown.
- Support:
  * SELECT
  * INSERT
  * UPDATE
  * DELETE
  * CREATE TABLE
  * ALTER TABLE
  * DROP TABLE
  * WHERE
  * ORDER BY
  * GROUP BY
  * HAVING
  * LIMIT
  * JOIN
  * COUNT, SUM, AVG, MAX, MIN
- If the user asks to create a table, generate a CREATE TABLE statement.
- Assume reasonable column names and data types when needed.

User Request:
{user_input}
"""

    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "Unable to generate SQL query."

    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""

    if request.method == "POST":
        user_input = request.form.get("query", "").strip()

        if user_input:
            output = generate_sql(user_input)

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)