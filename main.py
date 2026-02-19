from sensors import start_mqtt
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
