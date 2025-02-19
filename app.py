from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Initialize chatbot
chatbot = ChatBot(
    "PayPal Assistant",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///db.sqlite3"  # Persistent database
)

# Train chatbot only if database is empty
trainer = ChatterBotCorpusTrainer(chatbot)
if not chatbot.storage.count():
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

@app.route("/chat", methods=["POST"])
def get_bot_response():
    user_text = request.json.get("message")
    bot_response = chatbot.get_response(user_text)
    return jsonify({"response": str(bot_response)})

# Required for Vercel deployment
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)

if __name__ == "__main__":
    app.run(debug=True)
