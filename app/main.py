from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import psycopg2

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})
	

@app.post("/login")
async def user_login(username: str = Form(...), password: str = Form(...)):
	try:
		conn = psycopg2.connect(
			dbname="rpidb",
			user=username,
			password=password,
			host="0.0.0.0"
		)
		conn.close()
		return {"status":"success"}
	except Exception:
		raise HTTPException(status_code=401, detail="Invalid creds")
