from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from routers import blog, user
from utils import authenticate




app = FastAPI() 

#middleware
@app.middleware("http")
async def authenticateUser(request: Request, call_next):
    urlpath = request.url.path
    verb = request.method
    #print(verb, urlpath)
    if urlpath == "/login" or urlpath == "/docs" or urlpath=="/":
        response = await call_next(request)
        return response
    elif urlpath == "/user" and verb == "POST":
        response = await call_next(request)
        return response
    else:
        if request.headers.get("authorization"):
            if authenticate.authenticate_token(request.headers.get("authorization").split(" ")[1]) is None:
                return JSONResponse(content={"detail":"Expired Token"}) 
            else:       
                response = await call_next(request)
                return response
        else:
            return JSONResponse(content={"detail":"Token required"}) 
        
#routes
app.include_router(user.router)
app.include_router(blog.router)

#default route
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}




 



 
