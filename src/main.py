from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from groq import Groq
import requests
import json

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(
    title="Assistant de Codage IA API",
    description="API backend pour l'assistant de codage IA avec support Groq et HuggingFace",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration Groq
groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
# Configuration HuggingFace (alternative)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"

# Modèles Pydantic
class GenerateRequest(BaseModel):
    prompt: str
    code: Optional[str] = ""
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ExplainRequest(BaseModel):
    code: str
    context: Optional[str] = ""

class RefactorRequest(BaseModel):
    code: str
    instructions: Optional[str] = ""

class GenerateCodeRequest(BaseModel):
    description: str
    language: Optional[str] = "python"

class DetectBugsRequest(BaseModel):
    code: str

class OptimizeRequest(BaseModel):
    code: str

class GenerateResponse(BaseModel):
    response: str

class ExplainResponse(BaseModel):
    explanation: str

class RefactorResponse(BaseModel):
    refactored_code: str

class GenerateCodeResponse(BaseModel):
    code: str

class DetectBugsResponse(BaseModel):
    bugs: str

class OptimizeResponse(BaseModel):
    optimized_code: str

# Fonctions utilitaires
def call_groq_api(messages, max_tokens=1000, temperature=0.7):
    """Appel à l'API Groq"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile", # Ou un autre modèle Groq disponible
            max_tokens=max_tokens,
            temperature=temperature
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erreur Groq: {str(e)}")

def call_huggingface_api(prompt, max_tokens=1000):
    """Appel à l'API HuggingFace (alternative)"""
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(status_code=503, detail="Clé API HuggingFace non configurée")
    
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erreur HuggingFace: {str(e)}")

# Endpoints
@app.get("/")
async def root():
    return {"message": "Assistant de Codage IA API", "status": "active"}

@app.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    """Génère une réponse IA basée sur le prompt et le code"""
    messages = [
        {
            "role": "system",
            "content": "Tu es un assistant de codage IA expert. Tu aides les développeurs avec leurs questions de programmation, l'explication de code, la génération de code, et l'optimisation. Réponds toujours en français de manière claire et détaillée."
        },
        {
            "role": "user",
            "content": f"Code actuel:\n```\n{request.code}\n```\n\nQuestion: {request.prompt}"
        }
    ]
    
    response = call_groq_api(messages, request.max_tokens, request.temperature)
    return GenerateResponse(response=response)

@app.post("/explain", response_model=ExplainResponse)
async def explain_code(request: ExplainRequest):
    """Explique le code fourni"""
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en programmation. Explique le code de manière claire et détaillée, en décrivant ce que fait chaque partie importante. Réponds en français."
        },
        {
            "role": "user",
            "content": f"Explique ce code en détail:\n```\n{request.code}\n```\n\nContexte supplémentaire: {request.context}"
        }
    ]
    
    explanation = call_groq_api(messages)
    return ExplainResponse(explanation=explanation)

@app.post("/refactor", response_model=RefactorResponse)
async def refactor_code(request: RefactorRequest):
    """Refactorise le code selon les instructions"""
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en refactorisation de code. Améliore le code selon les instructions données, en gardant la même fonctionnalité mais en améliorant la lisibilité, les performances, ou la structure. Réponds uniquement avec le code refactorisé."
        },
        {
            "role": "user",
            "content": f"Refactorise ce code:\n```\n{request.code}\n```\n\nInstructions: {request.instructions}"
        }
    ]
    
    refactored = call_groq_api(messages)
    return RefactorResponse(refactored_code=refactored)

@app.post("/generate-code", response_model=GenerateCodeResponse)
async def generate_code(request: GenerateCodeRequest):
    """Génère du code basé sur une description"""
    messages = [
        {
            "role": "system",
            "content": f"Tu es un expert en programmation {request.language}. Génère du code propre, bien commenté et fonctionnel basé sur la description fournie. Réponds uniquement avec le code."
        },
        {
            "role": "user",
            "content": f"Génère du code {request.language} pour: {request.description}"
        }
    ]
    
    code = call_groq_api(messages)
    return GenerateCodeResponse(code=code)

@app.post("/detect-bugs", response_model=DetectBugsResponse)
async def detect_bugs(request: DetectBugsRequest):
    """Détecte les bugs potentiels dans le code"""
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en débogage. Analyse le code et identifie les bugs potentiels, les problèmes de sécurité, les erreurs logiques, et les améliorations possibles. Réponds en français."
        },
        {
            "role": "user",
            "content": f"Analyse ce code pour détecter les bugs:\n```\n{request.code}\n```"
        }
    ]
    
    bugs = call_groq_api(messages)
    return DetectBugsResponse(bugs=bugs)

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_code(request: OptimizeRequest):
    """Optimise le code fourni"""
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en optimisation de code. Améliore les performances, la lisibilité et l'efficacité du code tout en gardant la même fonctionnalité. Réponds uniquement avec le code optimisé."
        },
        {
            "role": "user",
            "content": f"Optimise ce code:\n```\n{request.code}\n```"
        }
    ]
    
    optimized = call_groq_api(messages)
    return OptimizeResponse(optimized_code=optimized)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


