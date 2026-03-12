from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import UserHealthInfo, RecommendationResponse
from .model_utils import get_recommendation

app = FastAPI(title="Personalized Medicine AI")

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Personalized Medicine Recommendation AI API"}

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(health_info: UserHealthInfo):
    result = get_recommendation(health_info)
    return result
