import os
import openai

from flask import Flask
from flask import request
from flask import render_template
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['user_input']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}  
        ]
    )
    recommendation = response.choices[0].text.strip()
    return render_template('recommendations.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run()
