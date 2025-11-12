from flask import Flask, render_template, request, jsonify
from ai.model import get_chatbot_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"\n📩 New message from {name} ({email}): {message}\n")
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    reply = get_chatbot_response(user_message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
