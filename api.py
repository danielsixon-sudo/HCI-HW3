import uvicorn
 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HCI Mini Review App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = [{
                "id": 0,
                "q": "Is Fitts' Law an example of a predictive model or a descriptive model?",
                "a": "Predictive model"
                },
             {
                "id": 1,
                "q": "Does this course focus more on genius design, systems design, or user-centered design?",
                "a": "User-centered design"
                },
             {
                "id": 2,
                "q": "What is the main goal of the ideation phase of iterative design?",
                "a": "Generating as many possible design solutions as possible"
                }
            ]

class QuestionRequest(BaseModel):
    question: str
    answer: str

# Resets the question IDs after a question has been removed
def reset_question_ids(questions): 
    id = 0
    for question in questions:
        question["id"] = id
        id = id + 1

@app.get("/questions")
def get_questions():
    return questions

@app.post("/add")
def add_question(req: QuestionRequest):
    questions.append({ 
        "id": len(questions),
        "q": req.question,
        "a": req.answer
    })

@app.delete("/delete/{id}")
def delete_question(id: int):
    # Check each question in the loop to find the ID
    for question in questions:
        if question["id"] == id:
            questions.remove(question)
            reset_question_ids(questions=questions)
            return
    # If the end of the loop is reached, the question is not in the list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")
    
@app.put("/update/{id}")
def update_question(id: int, req: QuestionRequest):
    # Check each question in the loop to find the ID
    for question in questions:
        if question["id"] == id:
            question["q"] = req.question
            question["a"] = req.answer
            return
    # If the end of the loop is reached, the question ID is not in the list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")

if __name__=="__main__":
    uvicorn.run(app, port=8005)