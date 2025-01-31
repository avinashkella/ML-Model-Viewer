from config import *
import os, textwrap, traceback
from openai import OpenAI

# Function to extract the model from the provided code
def extract_model_from_code(code_string):

    # Dictionary to serve as the execution context
    execution_context = {"num_classes": 10}

    try:
        # Normalize indentation using textwrap.dedent
        cleaned_code = textwrap.dedent(code_string).strip()

        # Attempt to execute the provided code
        exec(cleaned_code, execution_context)

        # Extract the model if it exists
        model = execution_context.get('model')
        print(model)
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

# Define a function to generate code using OpenAI
def generate_code(query):
    prompt = f"""
        Given the text below, generate the corresponding machine learning model in Python using a library such as TensorFlow or PyTorch. Return the code defining the model.
        All The variables including num_classes=10 inside code must be defined and code is executable without any error.

        Return a response like these examples:
        Text: i need a image model using tensorflow and keras.
        Model: {DEFAULT_CODE_KERAS}
        
        Text: i need a image model.
        Model: {DEFAULT_CODE_PYTORCH}

        Text: {query}
        Model:
    """

    try:
        # OpenAI API setup
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

    except Exception as e:
        return f"Error occurred: {e}"

    return answer