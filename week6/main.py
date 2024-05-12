# https://fastapi.tiangolo.com/
# https://ithelp.ithome.com.tw/m/articles/10325259?sc=rss.iron
# https://ithelp.ithome.com.tw/m/articles/10318017
# uvicorn main:app --reload

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")

# Add SessionMiddleware to the ASGI application
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

# connect to mysql
con=mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="website"
)

# Define a route handler for the root URL
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup", response_class=RedirectResponse)
async def verify_credentials(request: Request, name: str = Form(default=""), username: str = Form(default=""), password: str = Form(default="")):
    cursor=con.cursor()
    cursor.execute("select * from member where username=%s",(username,))
    result=cursor.fetchone()
    if result:
        cursor.close()
        return RedirectResponse(f"/error?message=帳號已經被註冊", status_code=303)
    
    cursor.execute("insert into member(name,username,password) values(%s,%s,%s)",(name,username,password))
    con.commit()
    cursor.close()
    return RedirectResponse("/", status_code=303)

@app.post("/signin", response_class=RedirectResponse)
async def verify_credentials(request: Request, username: str = Form(default=""), password: str = Form(default="")):
    if not username or not password:
        return RedirectResponse(f"/error?message=請輸入帳號、密碼", status_code=303) # status_code=303: let sign in know /error method is GET not POST
        
    else:
        cursor=con.cursor()
        cursor.execute("select * from member where username=%s and password=%s",(username,password))
        result=cursor.fetchone()
        cursor.close()
        if result:
            request.session["SIGNED-IN"] = True
            request.session["name"]=result[1]
            request.session["username"]=result[2]
            return RedirectResponse("/member", status_code=303)
        
        else:
            return RedirectResponse(f"/error?message=帳號或密碼輸入錯誤", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member_get(request: Request):
    if request.session.get("SIGNED-IN"):
        name = request.session.get("name", "")
        username = request.session.get("username", "")

        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="website"
        ) as conn:

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * from message")
                messages = cursor.fetchall()

        return templates.TemplateResponse("success.html", {"request": request, "name": name, "username":username, "messages":messages})
    else:
        return RedirectResponse("/", status_code=303)

@app.post("/createMessage")
async def create_message(request: Request, namem: str = Form(default=""), message: str = Form(default=""), usernamem: str = Form(default="")):
    if request.session.get("SIGNED-IN"):
        if message:
            cursor=con.cursor()
            cursor.execute("insert into message(name,message) values(%s,%s)",(namem,message))
            con.commit()
            cursor.close()
        return RedirectResponse("/member", status_code=303)
    
    return RedirectResponse("/", status_code=306)
    
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    # put error message into fail.html
    message = request.query_params.get("message", "")
    return templates.TemplateResponse("fail.html", {"request": request, "message": message})

@app.get("/signout", response_class=RedirectResponse)
async def signout(request: Request):
    request.session["SIGNED-IN"] = False
    return RedirectResponse("/", status_code=303)

# Cache: If you've made changes to the CSS file after loading the page, your browser might still be using a cached version of the file. Try clearing your browser cache or performing a hard refresh (Ctrl + F5 or Cmd + Shift + R) to ensure that the latest CSS styles are loaded.