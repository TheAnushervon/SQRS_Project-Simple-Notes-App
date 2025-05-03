from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/templates/login.html", "r") as file: 
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200) 


@app.get("/register", response_class=HTMLResponse)
async def register(): 
    with open("app/templates/register.html", "r") as file: 
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200) 