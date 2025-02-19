from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

app = Flask(__name__)

# Initialize chatbot with database storage
chatbot = ChatBot(
    "PayPal Assistant",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///database.sqlite3"
)

# Train chatbot only if database doesn't exist
if not os.path.exists("database.sqlite3"):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english",
        "chatterbot.corpus.english.ai",
        "chatterbot.corpus.english.computers",
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.science"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_text = request.args.get("msg", "").strip()
    if not user_text:
        return "Please type a message."
    
    try:
        response = str(chatbot.get_response(user_text))
    except Exception as e:
        response = "I'm having trouble understanding right now. Please try again."
    
    return response

# For Vercel deployment
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)
