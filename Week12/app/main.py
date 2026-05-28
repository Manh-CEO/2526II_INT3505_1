from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import HTMLDesponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Week 12 - API as a Product Demo")
templates = Jinja2Templates(directory="Week12/app/templates")

API_KEYS = {
    "demo_key_12345": {"owner": "Acme Corp", "limit": 1000, "usage": 42}
}
 API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key in API_KEYS:
        return api_key
    raise HTTPException(status_code=403, detail="API Key khong hop le.")

@app.get("/", response_class=HTMLResponse)
async def developer_portal(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request})

@app.get("/api/v1/weather")
async def get_weather(city: str, api_key: str = Depends(get_api_key)):
    API_KEYS[api_key]["usage"] += 1
    return {
        "city": city,
        "temperature": 32,
        "condition": "Cloudy",
        "credits_left": API_KEYS[api_key]["limit"] - API_KEYS[api_key]["usage"]
    }

@app.get("/api/usage")
async def get_usage(api_key: str):
    if api_key not in API_KEYS:
        return {"error": "Invalid Key"}
    return {"total_calls": API_KEYS[api_key]["usage"]}

imf __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
