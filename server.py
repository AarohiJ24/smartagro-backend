from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from predict.mainfn import recommend_crop

app = FastAPI()

# Allow requests from your frontend (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SmartAgro Backend is running!"}

@app.post("/recommend-crop/")
async def recommend(data: dict):
    state = data.get("state")
    if not state:
        raise HTTPException(status_code=400, detail="State is required")

    try:
        result = recommend_crop(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
