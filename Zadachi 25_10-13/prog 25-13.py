from wsgiref.simple_server import make_server
import json
import random
import time
import requests

CLIENTS_REQUIRED = 2
TIME_LIMIT = 10
clients = []
scores = {}

# Load questions from file
with open("questions.json", "r") as f:
    questions = json.load(f)

def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    
    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            request_body = environ["wsgi.input"].read(content_length)
            data = json.loads(request_body)
        except:
            data = {}
    else:
        data = {}
    
    if path == "/connect" and method == "POST":
        client_id = data.get("client_id")
        if client_id not in clients:
            clients.append(client_id)
            scores[client_id] = 0
        
        response_body = json.dumps({"message": "All clients connected. Quiz starting soon." if len(clients) >= CLIENTS_REQUIRED else "Waiting for more clients"})
    
    elif path == "/get_question" and method == "GET":
        client_id = environ.get("QUERY_STRING", "").split("=")[1] if "=" in environ.get("QUERY_STRING", "") else ""
        if len(clients) < CLIENTS_REQUIRED:
            response_body = json.dumps({"message": "Waiting for more clients"})
        else:
            question = random.choice(questions)
            response_body = json.dumps(question)
    
    elif path == "/submit_answer" and method == "POST":
        client_id = data.get("client_id")
        answer = data.get("answer")
        question_text = data.get("question")
        
        question = next((q for q in questions if q["question"] == question_text), None)
        if question:
            selected_answers = set(answer)
            correct_answers = set(question["correct"])
            if selected_answers == correct_answers:
                scores[client_id] += 1
        
        response_body = json.dumps({"message": "Answer received"})
    
    elif path == "/get_score" and method == "GET":
        client_id = environ.get("QUERY_STRING", "").split("=")[1] if "=" in environ.get("QUERY_STRING", "") else ""
        response_body = json.dumps({"score": scores.get(client_id, 0)})
    
    else:
        response_body = json.dumps({"error": "Invalid request"})
    
    start_response("200 OK", [("Content-Type", "application/json")])
    return [response_body.encode()]

if __name__ == "__main__":
    server = make_server("0.0.0.0", 6000, application)
    print("[*] WSGI server running on port 6000...")
    server.serve_forever()

