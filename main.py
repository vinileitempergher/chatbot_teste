from flask import Flask
from app.bot import bot

app = Flask(__name__)

app.add_url_rule('/bot', 'bot', bot, methods=['POST'])
app.add_url_rule('/', 'index', lambda: "Funcionou", methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
