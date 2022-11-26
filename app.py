from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/")
async def index(req:Request, db:Session = Depends(get_db)):
    data = db.query(models.Todos).all()
    return templates.TemplateResponse("base.html", {"request": req, "todos": data })

@app.post("/insert")
def insert(req:Request, work: str = Form(...), db:Session = Depends(get_db)):
    todo = models.Todos(work=work)
    db.add(todo)
    db.commit()
    url = app.url_path_for("index")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/update/{id}")
def update(req:Request, id: int, work: str = Form(...), db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == id).first()
    todo.work = work
    db.commit()
    url = app.url_path_for("index")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/complete/{id}")
def complete(req:Request, id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == id).first()
    todo.complete = True
    db.commit()
    url = app.url_path_for("index")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{id}")
def delete(req:Request, id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("index")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)