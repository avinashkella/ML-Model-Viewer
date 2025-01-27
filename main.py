import os
from flask import Flask, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()


# pylint: disable=C0103
app = Flask(__name__)
app.config["DEBUG"] = False


@app.route("/", methods=["POST"])
def generateCode():

    request_body = request.form

    query = request_body.get("prompt")

    prompt = f"""
        Given the text below, generate the corresponding machine learning model in Python using a library such as TensorFlow or PyTorch. Return only the code defining the model.

        Text: {query}

        Model:
        """

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("organization"),
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        answer = response.choices[0].message.content.strip()
        print(answer)

    except Exception as e:
        print("Error due to ", e)

    return answer


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))