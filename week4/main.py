# https://fastapi.tiangolo.com/
# https://ithelp.ithome.com.tw/m/articles/10325259?sc=rss.iron
# https://ithelp.ithome.com.tw/m/articles/10318017
# uvicorn main:app --reload

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")

# Add SessionMiddleware to the ASGI application
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

# Define a route handler for the root URL
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

error_message=""

@app.post("/signin", response_class=RedirectResponse)
async def verify_credentials(request: Request, username: str = Form(default=""), password: str = Form(default=""), checkbox: bool = Form(default=False)):
    if not username or not password:
        error_message="請輸入帳號、密碼"
        return RedirectResponse(f"/error?message={error_message}", status_code=303) # status_code=303: let sign in know /error method is GET not POST
        
    elif username == "test" and password == "test":
        request.session["SIGNED-IN"] = True
        return RedirectResponse("/member", status_code=303)
    
    else:
        error_message="帳號、密碼輸入錯誤"
        return RedirectResponse(f"/error?message={error_message}", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member_get(request: Request):
    if request.session.get("SIGNED-IN"):
        return templates.TemplateResponse("success.html", {"request": request})
    else:
        return RedirectResponse("/")

# @app.route("/error", methods=["GET", "POST"])
# async def error(request: Request):
#     # put error_message into fail.html
#     message = request.query_params.get("message", "")
#     if request.method == "GET":
#         return templates.TemplateResponse("fail.html", {"request": request, "message": message}, status_code=200)
#     elif request.method == "POST":
#         return templates.TemplateResponse("fail.html", {"request": request, "message": message}, status_code=405)

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    # put error_message into fail.html
    message = request.query_params.get("message", "")
    return templates.TemplateResponse("fail.html", {"request": request, "message": message})

@app.get("/signout", response_class=RedirectResponse)
async def signout(request: Request):
    request.session["SIGNED-IN"] = False
    return RedirectResponse("/")

# Cache: If you've made changes to the CSS file after loading the page, your browser might still be using a cached version of the file. Try clearing your browser cache or performing a hard refresh (Ctrl + F5 or Cmd + Shift + R) to ensure that the latest CSS styles are loaded.