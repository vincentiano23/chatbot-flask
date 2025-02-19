import os
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Initialize chatbot with persistent database
chatbot = ChatBot("PayPal Assistant", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///database.sqlite3")

# Train the bot only if database does not exist
if not os.path.exists("database.sqlite3"):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english",
        "chatterbot.corpus.english.ai",
        "chatterbot.corpus.english.computers",
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.science"
    )
    print("Training completed!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_text = request.args.get("msg")
    return str(chatbot.get_response(user_text))

# Ensure the app is only run locally, not in production (Vercel handles execution)
if __name__ == "__main__":
    app.run(debug=True)
