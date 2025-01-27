import os
from flask import Flask, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import ast

load_dotenv()


# pylint: disable=C0103
app = Flask(__name__)
app.config["DEBUG"] = False

def extract_model_from_code(code_string):
    import traceback
    import textwrap

    # Dictionary to serve as the execution context
    execution_context = {}

    try:
        # Normalize indentation using textwrap.dedent
        cleaned_code = textwrap.dedent(code_string).strip()

        # Attempt to execute the provided code
        exec(cleaned_code, execution_context)

        # Extract the model if it exists
        model = execution_context.get('model')

        if model:
            print("Model extracted successfully:")
            return model
        else:
            print("No model found in the provided code.")
            return None

    except Exception as e:
        # Print error traceback for debugging
        print("An error occurred while executing the code:")
        traceback.print_exc()
        return None

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

    model = extract_model_from_code(answer)

    if model:
        print("Model extracted successfully and here to use it")
    else:
        print("Failed to extract model.")

    return model


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))