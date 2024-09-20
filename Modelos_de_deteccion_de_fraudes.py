from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import speech_recognition as sr
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize recognizer
r = sr.Recognizer()

# Read the system message
with open('C://Users//ferna//repos//SpechToTextWeb//rootPromt.txt', 'r', encoding="utf-8") as file:
    rootPromt = file.read()

# Set OpenAI API key
openai.api_key = "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"

messages = [
    {"role": "system", "content": rootPromt}
]

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Use the microphone as input source
        with sr.Microphone() as source2:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # Listen for user input
            print("Listening...")
            audio2 = r.listen(source2, phrase_time_limit=5)
            print("Finished listening...")

            # Recognize the speech using Google Speech Recognition
            MyText = r.recognize_google(audio2, language="es-MX").lower()
            print(f"Recognized text: {MyText}")

            # Call the OpenAI API with the recognized text
            messages.append({"role": "user", "content": f"<conversacion>{MyText}</conversacion>"})
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Return the response from the model
            response_text = completion.choices[0].message['content']
            return jsonify({"response": response_text})

    except sr.RequestError as e:
        return jsonify({"error": f"Request error: {e}"})

    except sr.UnknownValueError:
        return jsonify({"error": "Unknown error occurred in speech recognition"})


if __name__ == '__main__':
    app.run(debug=True)