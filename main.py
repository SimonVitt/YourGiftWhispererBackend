from flask import Flask, request
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS 

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app, origins="https://yourgiftwhisperer.com")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/getidea", methods=["POST"])
def get_idea():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = openai.Completion.create(
            model="babbage:ft-personal:babbage-second-giftwhisperer-2023-05-22-22-52-23",
            prompt="Provide four unique gift suggestions for the specified person in a JSON array format, without additional comments(most important)!! Each entry should have 'title', 'description', and 'amazonlink' fields. Adhere strictly to any given price range. The 'amazonlink' should be an Amazon search URL with the gift's name replacing 'giftname' in this template: 'https://assoc-redirect.amazon.com/g/r/https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=giftname&tag=giftwhisper0f-20'. Always return only the JSON array!! Structure example: `[{\"title\": \"title\", \"description\": \"description\", \"amazonlink\": \"amazonlink\"},...]`." + f"Give me gift ideas for a person,which is described as: {user_input} ->",
            max_tokens = 1200,
            temperature=0.8
        )
        try:
            with open("usercommunication.txt", "a") as file:
                file.write(user_input, "++++", response["choices"][0]["text"])
        except Exception as e:
            print(e)
        return response
    
@app.route("/get_more_ideas", methods=["POST"])
def get_more_ideas():
    if request.method == 'POST':
        user_input = request.form['user_input']
        currentideas = request.form['currentideas']
        print(currentideas)
        response = openai.Completion.create(
            model="babbage:ft-personal:babbage-second-giftwhisperer-2023-05-22-22-52-23",
            prompt="Provide four unique gift suggestions for the specified person in a JSON array format, without additional comments(most important)!! Each entry should have 'title', 'description', and 'amazonlink' fields. Adhere strictly to any given price range. The 'amazonlink' should be an Amazon search URL with the gift's name replacing 'giftname' in this template: 'https://assoc-redirect.amazon.com/g/r/https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=giftname&tag=giftwhisper0f-20'. Always return only the JSON array!! Structure example: `[{\"title\": \"title\", \"description\": \"description\", \"amazonlink\": \"amazonlink\"},...].`" + f"Give me gift ideas for a person,which is described as: {user_input} \n but these shouldnt contain any of the following ideas {currentideas}  ->",
            max_tokens=700,
            temperature=0.8
        )
        return response