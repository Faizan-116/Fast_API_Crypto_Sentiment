# main.py
from fastapi import FastAPI,status
from pydantic import BaseModel








app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello TutLinks.com"}


class findhas(BaseModel):
    InputText: str
     



     
#function to extract hastags
def sentiment_scores(Curency):
     
    
    return Curency



#api for find sentiment in the text
@app.post("/findsentiment", status_code=status.HTTP_201_CREATED)
def sentiment(User: findhas):
    return sentiment_scores(User.InputText)