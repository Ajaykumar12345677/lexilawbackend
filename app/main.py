from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.matcher import matcher
from app.services.simplifier import simplifier
from app.services.guidance import guidance_service
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="LexiLaw API", description="AI-powered legal awareness")

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    problem: str

class MatchResult(BaseModel):
    code: str
    title: str
    description: str  # Original Legal Text
    simplified_explanation: str
    punishment: str
    bailable: str
    cognizable: str
    court: str
    guidance: List[str]
    score: float 

class ResponseModel(BaseModel):
    matched_sections: List[MatchResult]

@app.get("/")
def read_root():
    return {"message": "LexiLaw Backend is Running"}

@app.post("/analyze", response_model=ResponseModel)
def analyze_problem(input_data: UserInput):
    problem = input_data.problem
    if not problem:
        raise HTTPException(status_code=400, detail="Problem description cannot be empty")
    
    # Semantic Matching
    matches = matcher.search(problem, top_k=3, threshold=0.2) 
    
    results = []
    
    for match in matches:
        item = match['section']
        score = match['score']
        
        # 1. Descriptions
        original_desc = item.get('description', 'No description available.')
        
        # PREFER existing manual simplified description if available
        existing_simple = item.get('simple_desc', '')
        if existing_simple and len(existing_simple) > 10:
             simplified = existing_simple
        else:
             # Fallback to AI simplification only if manual is missing
             simplified = simplifier.simplify(original_desc[:512])

        # 2. Guidance (Use improved logic)
        guidance_steps = guidance_service.get_guidance(item, problem)
        
        results.append(MatchResult(
            code=item.get('code', 'Unknown'),
            title=item.get('title', 'Unknown Title'),
            description=original_desc,
            simplified_explanation=simplified,
            punishment=item.get('punishment', 'Not specified'),
            bailable=item.get('bailable', 'Not specified'),
            cognizable=item.get('cognizable', 'Not specified'),
            court=item.get('court', 'Not specified'),
            guidance=guidance_steps,
            score=score
        ))
        
    return ResponseModel(matched_sections=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
