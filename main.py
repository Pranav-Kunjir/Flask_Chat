from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necessary for using sessions

@app.route('/', methods=['GET'])
def chat():
    # Initialize session messages if not already
    if 'messages' not in session:
        session['messages'] = []
    return render_template('hello.html', messages=session['messages'])

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        timestamp = datetime.now().strftime('%H:%M')
        session['messages'].append({
            'text': message,
            'timestamp': timestamp,
            'sender': 'user'
        })

        # Generate response using the AI model
        response = model.generate_content(message)
        session['messages'].append({
            'text': response.text,
            'timestamp': timestamp,
            'sender': 'bot'
        })

        session.modified = True  # Save session changes

    # Return JSON response
    return jsonify(messages=session['messages'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200)
