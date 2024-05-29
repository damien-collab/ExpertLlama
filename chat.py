import os
from groq import Groq



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

MODEL = 'llama3-8b-8192'

MODEL = 'llama3-70b-8192'

MODEL = 'mixtral-8x7b-32768'


class ChatBot:
    def __init__(self, api_key, model, max_tokens, system_prompt, window_size=20):
        self.client = Groq(api_key=os.environ.get(api_key))
        self.model = model
        self.max_tokens = max_tokens
        self.window_size = window_size
        self.messages = [
            # {"role": "system", "content": "You are an expert assistant that is highly intelligent and applies first principle thinking. Use your expertise in well-written intellectual responses (with optionally a little bit of witty humor, if that helps in the reponse and is appropiate). If you are not familiar with the topic or need additional info, just say it! Keep your responses very short and very consise."}
            {"role": "system", "content": system_prompt}
        ]


    def chat(self, user_input):
        if user_input.lower() in ["exit", "quit"]:
            pass

        self.messages.append({"role": "user", "content": user_input})
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size:]
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            max_tokens=self.max_tokens,
            stream=False,
            temperature=0.9,
        )
        assistant_response = chat_completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_response})
        # print(f"Assistant: {assistant_response}")
        return assistant_response
    

    def get_transcript(self):
        transcript_lines = []
        for message in self.messages:
            if message['role'] == 'user':
                transcript_lines.append('**User:**\n' + message['content'])
            elif message['role'] == 'assistant':
                transcript_lines.append('**Assistant:**\n' + message['content'])
        transcript_all_messages = '\n\n'.join(transcript_lines)
        return transcript_all_messages



# Example usage
# chatbot = ChatBot(api_key='GROQ_API_KEY', model='llama3-8b-8192', max_tokens=4000)

# chatbot.chat('Explain blockcain')



# chatbot.chat('summarise')



# import json

# def get_weather(city_name):
#     """Get the current weather for a given city."""
#     weather_data = {
#         "New York": {"temperature": 70, "condition": "Sunny"},
#         "Los Angeles": {"temperature": 75, "condition": "Partly Cloudy"},
#         "Chicago": {"temperature": 65, "condition": "Rainy"},
#     }
#     return json.dumps(weather_data.get(city_name, {"error": "City not found"}))

# def run_weather_conversation(user_prompt):
#     messages = [
#         {"role": "system", "content": "You are a function calling LLM that uses the data extracted from the get_weather function to answer questions about weather."},
#         {"role": "user", "content": user_prompt},
#     ]
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_weather",
#                 "description": "Get the current weather for a given city",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "city_name": {"type": "string", "description": "The name of the city (e.g., 'New York')"},
#                     },
#                     "required": ["city_name"],
#                 },
#             },
#         }
#     ]
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",
#         max_tokens=4096
#     )

#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls
#     if tool_calls:
#         available_functions = {"get_weather": get_weather}
#         messages.append(response_message)
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)
#             function_response = function_to_call(city_name=function_args.get("city_name"))
#             messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": function_response})
#         second_response = client.chat.completions.create(model=MODEL, messages=messages)
#         return second_response.choices[0].message.content

# user_prompt = "What is the weather in New York? And that of Chicago?"
# print(run_weather_conversation(user_prompt))






# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer

# class RAGSystem:
#     def __init__(self, documents):
#         self.documents = documents
#         self.vectorizer = TfidfVectorizer()
#         self.document_matrix = self.vectorizer.fit_transform(documents)

#     def retrieve(self, query):
#         query_vec = self.vectorizer.transform([query])
#         similarities = cosine_similarity(query_vec, self.document_matrix).flatten()
#         most_similar_idx = similarities.argmax()
#         return self.documents[most_similar_idx], similarities[most_similar_idx]

# def run_rag_conversation(user_prompt, rag_system):
#     retrieved_doc, similarity_score = rag_system.retrieve(user_prompt)
#     messages = [
#         {"role": "system", "content": "You are an expert assistant that uses retrieved documents to provide detailed and accurate answers."},
#         {"role": "user", "content": user_prompt},
#         {"role": "system", "content": f"Retrieved document (similarity score: {similarity_score}): {retrieved_doc}"}
#     ]
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         max_tokens=4096
#     )
#     return response.choices[0].message.content

# # Example data
# documents = [
#     "'Bitcoin breaks 100k$ as market cap reaches 2 trillion'",
#     "Ethereum is currently at 100K$ as market cap reaches 1 trillion",
#     "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
#     "Machine learning is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention."
# ]

# rag_system = RAGSystem(documents)
# user_prompt = "Hoeveel is Etheruem waard?."
# print(run_rag_conversation(user_prompt, rag_system))







# from typing import Any, Dict, Optional
# import json
# from jsonschema import validate, ValidationError as JSONSchemaValidationError
# import os
# from groq import Groq

# # Initialize the Groq client
# groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# def fetch_data(schema: Dict[str, Any], prompt: str) -> Optional[Dict[str, Any]]:
#     schema_json = json.dumps(schema, indent=2)
#     chat_completion = groq.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a database that outputs data in JSON format.\n"
#                     f"The JSON object must strictly follow this schema:\n{schema_json}\n"
#                     "Generate the actual data, not the schema."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": prompt,
#             },
#         ],
#         model="llama3-8b-8192",
#         temperature=0,
#         stream=False,
#         response_format={"type": "json_object"},
#     )

#     try:
#         response_content = chat_completion.choices[0].message.content
#         data = json.loads(response_content)
#         validate(instance=data, schema=schema)  # Validate the JSON data against the schema
#         return data
#     except (json.JSONDecodeError, JSONSchemaValidationError) as e:
#         print(f"Error parsing data: {e}")
#         print("Response content was:", response_content)
#         return None

# def print_data(data: Dict[str, Any]):
#     if data:
#         print(json.dumps(data, indent=2))
#     else:
#         print("No valid data found.")

# # Example usage for dynamically defined schemas
# recipe_schema = {
#     "type": "object",
#     "properties": {
#         "recipe_name": {"type": "string"},
#         "ingredients": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "properties": {
#                     "name": {"type": "string"},
#                     "quantity": {"type": "string"},
#                     "quantity_unit": {"type": "string"},
#                 },
#                 "required": ["name", "quantity"],
#             },
#         },
#         "directions": {
#             "type": "array",
#             "items": {"type": "string"},
#         },
#     },
#     "required": ["recipe_name", "ingredients", "directions"],
# }

# weather_schema = {
#     "type": "object",
#     "properties": {
#         "location": {"type": "string"},
#         "temperature": {"type": "number"},
#         "condition": {"type": "string"},
#     },
#     "required": ["location", "temperature", "condition"],
# }

# # Function to dynamically use the fetch_data function
# def dynamic_usage(schema: Dict[str, Any], prompt: str):
#     data = fetch_data(schema, prompt)
#     print_data(data)

# # Example: Fetching a recipe
# dynamic_usage(recipe_schema, "Fetch a recipe for apple pie")

# # Example: Fetching weather data
# dynamic_usage(weather_schema, "Fetch the current weather for New York City")

