from dotenv import load_dotenv
import os
import json
from openai import OpenAI

print("Script started")

# Load environment variables from .env file
load_dotenv("C:\\CanCode\\FUNCTION-CALLING-ASSIGNMENT\\Function-calling\\adapi.env")

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

# Create an OpenAI client
client = OpenAI(api_key=api_key)

# Define functions
def read_file():
    """Simulate reading data from a file"""
    return json.dumps({"result": "Data read from file: ['line1', 'line2', 'line3']"})

def query_database():
    """Simulate querying a database"""
    return json.dumps({"result": "Database query result: {'id': 101, 'name': 'Alice'}"})

def network_request():
    """Simulate making a network request"""
    return json.dumps({"result": "Network request response: {'status': 200, 'content': 'Success'}"})

# Function to handle the conversation
def run_conversation():
    print("Inside run_conversation")
    functions = [
        {
            "name": "read_file",
            "description": "Read data from a file",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "query_database",
            "description": "Query a database",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "network_request",
            "description": "Make a network request",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    ]

    messages = [{"role": "user", "content": "Please read data from a file, query the database, and make a network request. Then summarize the results."}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    response_message = response.choices[0].message
    print("Initial response:")
    print(json.dumps(response_message.model_dump(), indent=4))

    print("Calling all functions:")
    for func_name in ["read_file", "query_database", "network_request"]:
        function_to_call = globals()[func_name]
        function_response = function_to_call()
        print(f"{func_name} response:")
        print(function_response)
        messages.append({
            "role": "function",
            "name": func_name,
            "content": function_response
        })
    
    # Get a final response from the model
    try:
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
        )
        final_message = final_response.choices[0].message
        print("Final response:")
        print(json.dumps(final_message.model_dump(), indent=4))
    except Exception as e:
        print(f"Error getting final response: {str(e)}")
        final_message = None

    return final_message

# In the main block:
if __name__ == "__main__":
    try:
        result = run_conversation()
        print("Conversation completed successfully.")
        if result:
            print("Final result:")
            print(json.dumps(result.model_dump(), indent=4))
        else:
            print("No final result available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

print("Script ended")