from nicegui import ui
import requests

API_URL = "http://localhost:8005"

questions = []
page_body = ui.column().classes('w-full justify-center items-center')

def api_get(path):
    try:
        # Attempt to send GET request to API
        response = requests.get(f"{API_URL}{path}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, GET was successful so return response data
        return response.json()
    except requests.RequestException as e:
        # GET request was unsuccessful
        # Send an alert with error details to the UI and return empty list
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []

def api_post(path, data):
    try:
        # Attempt to send POST request to API with data payload
        response = requests.post(f"{API_URL}{path}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, POST was successful so return True
        return True
    except requests.RequestException as e:
        # POST request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

def api_delete(path, id):
    try:
        # Attempt to send a DELETE request to API
        response = requests.delete(f"{API_URL}{path}/{id}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, DELETE was successful so return True
        return True
    except requests.RequestException as e: 
        # DELETE request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False


def api_put(path, id, data):
    try:
        # Attempt to send UPDATE request to API with data payload
        response = requests.put(f"{API_URL}{path}/{id}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, UPDATE was successful so return True
        return True
    except requests.RequestException as e:
        # UPDATE request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

def render_question(question):
    with ui.card().classes("w-130") as card:
        card.on("click", lambda: toggle_answer(question["id"]))
        ui.label(question["q"]).classes("text-lg")
        ui.label(question["a"]).classes("text-lg text-green font-bold").bind_visibility_from(question["state"], "show_answer")
        
        with ui.dialog() as dialog, ui.card():
            # Allow the user to enter a question
            ui.label("Update Question").classes("text-2xl font-bold")
            ui.label("Question:").classes("text-lg font-bold")
            updated_question = ui.textarea(value=question["q"]).classes("w-96 text-lg bg-blue-50 p-4 border-2 border-black-500")

            # Allow the user to enter an answer
            ui.label("Answer:").classes("text-lg font-bold")
            updated_answer = ui.textarea(value=question["a"]).classes("w-96 text-lg bg-blue-50 p-4 border-2 border-black-500")

            # Logic for updating question after pressing update button
            ui.button('Update question', on_click=lambda: [
                dialog.close(),
                api_put("/update", question["id"],{
                    "question": updated_question.value,
                    "answer": updated_answer.value,
                }),
                render_page()
            ])

        # Place the edit and delete buttons in a row
        with ui.row():
            edit_question_btn = ui.button(text="Edit", color="#BDEBF9", on_click=dialog.open)
            delete_question_btn = ui.button(text="Delete", color="#F9BDC1", on_click=lambda: delete_question(id=question["id"])).classes('ml-4')
        
     
def toggle_answer(i):
    questions[i]["state"]["show_answer"] = not questions[i]["state"]["show_answer"]

def add_new_question(question, answer):
    api_post("/add", {"question": question, "answer": answer})
    render_page()

def delete_question(id):
    api_delete(f"/delete", id)
    render_page()    

def render_text_inputs():
    new_question_input = ui.input(label="New question").props("clearable").classes("w-96 text-lg bg-blue-50 p-4 border-2 border-black-500")
    new_answer_input = ui.input(label="New answer").props("clearable").classes("w-96 text-lg bg-blue-50 p-4 border-2 border-black-500")
    add_question_btn = ui.button(text="Add question", on_click=lambda: add_new_question(
        question=new_question_input.value,
        answer=new_answer_input.value
    ))

def init_page():
    render_page()

def render_page():
    global questions
    questions = api_get("/questions")
    page_body.clear()
    with page_body:
        ui.label("Create a New Question").classes('text-5xl font-bold mt-10 mb-5')
        render_text_inputs()
        ui.label("Saved Questions").classes('text-5xl font-bold mt-20 mb-8')
        for question in questions:
            question["state"] = {"show_answer": False}
            render_question(question)
            

init_page()
ui.run(port=8084, title="HCI Review Application")