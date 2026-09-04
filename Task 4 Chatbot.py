import re
import logging
from datetime import datetime


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = " ".join(text.split())
    return text


session = {
    "name": None,
    "last_intent": None,
    "running": True
}


intent_map = {
    "greeting": ["hello", "hi", "hey", "salam"],
    "help": ["help", "menu", "what can you do"],
    "name": ["my name is", "i am", "call me"],
    "time": ["time", "current time", "what time is it"],
    "thanks": ["thanks", "thank you"],
    "bye": ["bye", "goodbye", "exit", "quit"]
}


def detect_intent(user_input):
    for intent, keywords in intent_map.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent

    return "unknown"


def handle_greeting():
    if session["name"] is not None:
        return f"Hello, {session['name']}! 👋 How can I help you?"

    return "Hello! 👋 How can I help you?"


def handle_help():
    return (
        "I can help you with:\n"
        "1. Greetings\n"
        "2. Your name\n"
        "3. Current time\n"
        "4. Thanks\n"
        "5. Exit the chatbot"
    )


def handle_time():
    current_time = datetime.now().strftime("%I:%M %p")

    if session["name"] is not None:
        return f"{session['name']}, the current time is {current_time}."

    return f"The current time is {current_time}."


def handle_bye():
    session["running"] = False
    return "Goodbye! Have a nice day. 👋"


def handle_name(user_input):
    patterns = [
        r"my name is (.+)",
        r"i am (.+)",
        r"call me (.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input)

        if match:
            name = match.group(1).strip().title()
            session["name"] = name
            return f"Nice to meet you, {name}! 😊"

    return "I couldn't understand your name."


def handle_thanks():
    if session["name"] is not None:
        return f"You're welcome, {session['name']}! 😊"

    return "You're welcome! 😊"


handlers = {
    "greeting": handle_greeting,
    "help": handle_help,
    "name": handle_name,
    "time": handle_time,
    "thanks": handle_thanks,
    "bye": handle_bye
}


def route_intent(intent, user_input):
    if intent == "name":
        return handle_name(user_input)

    elif intent in handlers:
        return handlers[intent]()

    elif session["name"] is not None:
        return f"Sorry {session['name']}, I didn't understand that. You can type 'help' to see my options."

    else:
        return "Sorry, I didn't understand that. You can type 'help' to see my options."


logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


print("🤖 Chatbot started!")
print("Type 'help' to see what I can do.")
print("Type 'bye' to exit.\n")


while session["running"]:
    user_input = input("You: ")

    normalized_input = normalize_text(user_input)

    if normalized_input == "":
        print("Bot: Please type something.")
        continue

    intent = detect_intent(normalized_input)

    session["last_intent"] = intent

    response = route_intent(intent, normalized_input)

    print("Bot:", response)

    logging.info(
        "User: %s | Intent: %s | Bot: %s",
        user_input,
        intent,
        response
    )