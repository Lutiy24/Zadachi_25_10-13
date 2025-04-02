# Client Code
def client_program(server_url, client_id):
    import time
    
    # Connect to server
    response = requests.post(f"{server_url}/connect", json={"client_id": client_id})
    print(response.json()["message"])
    while "Waiting" in response.json()["message"]:
        time.sleep(2)
        response = requests.post(f"{server_url}/connect", json={"client_id": client_id})
    
    # Answer questions
    for _ in range(3):
        response = requests.get(f"{server_url}/get_question?client_id={client_id}")
        question_data = response.json()
        if "message" in question_data:
            print(question_data["message"])
            break
        
        print(f"\n{question_data['question']}")
        for i, option in enumerate(question_data['options'], 1):
            print(f"{i}. {option}")
        
        answer_indices = input("Enter your answers (comma separated): ")
        selected_answers = [question_data['options'][int(i)-1] for i in answer_indices.split(',') if i.isdigit()]
        requests.post(f"{server_url}/submit_answer", json={"client_id": client_id, "question": question_data['question'], "answer": selected_answers})
    
    # Get final score
    response = requests.get(f"{server_url}/get_score?client_id={client_id}")
    print("Final Score:", response.json()["score"])

if __name__ == "__main__":
    client_id = input("Enter your client ID: ")
    server_url = "http://127.0.0.1:6000"
    client_program(server_url, client_id)