
# ------ Code for Web Dashboard Interface -------

from flask import Flask, render_template, request, jsonify
from data_manager import get_combined_data
from ai_advisor import generate_ai_advice
import socket

app = Flask(__name__)


# ===============================
# HOME PAGE
# ===============================

@app.route("/")
def home():
    data = get_combined_data()
    return render_template("index.html", data=data)


# ===============================
# AI CHAT ENDPOINT
# ===============================

@app.route("/ask", methods=["POST"])
def ask():
    farmer_question = request.json.get("question")

    combined_data = get_combined_data()
    answer = generate_ai_advice(combined_data, farmer_question)

    return jsonify({"answer": answer})

# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("\n===================================")
    print(f"🌐 Open this in browser:")
    print(f"http://{local_ip}:5000")
    print("===================================\n")

    app.run(host="0.0.0.0", port=5000, debug=False)






'''from sensors import start_mqtt
from data_manager import get_combined_data
from ai_advisor import generate_ai_advice
import time

start_mqtt()

data = get_combined_data()

farmer_question = input("Ask your farming question: ")
time.sleep(0.5)
answer = generate_ai_advice(data, farmer_question)
time.sleep(1)
print("\nAI Response:\n")
print(answer)
'''
