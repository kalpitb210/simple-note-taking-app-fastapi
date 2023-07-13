from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import datetime
from fastapi.staticfiles import StaticFiles

# to delete a note
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb+srv://notes:kalpit_123@notes.kadxk3o.mongodb.net/")
db = client["notes"]
notes_collection = db["notes"]

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="style.css")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/")
def read_root(request: Request):
    notes = notes_collection.find()
    print(notes)
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

impotance = ""
@app.post("/submit")
def submit_note(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    important: bool = Form(False)
):
    if important == True:
        importance = "Yes"
    else:
        importance = "No"
    note = {"title": title, "description": description, "important": importance, "datetime": current_datetime}
    notes_collection.insert_one(note)
    return read_root(request)


@app.post("/delete-all")
def delete_all_notes(request: Request):
    result = notes_collection.delete_many({})
    return read_root(request)

@app.post("/delete-note/{note_id}")
def delete_note(request: Request, note_id: str):
    print(type(note_id))
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})

    if result.deleted_count == 1:
        print('Document deleted successfully.')
    else:
        print('Document not found.')    
    
    return read_root(request)




