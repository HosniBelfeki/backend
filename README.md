# 🔧 Backend - Assistant de Codage IA

API REST construite avec FastAPI et intégration OpenAI pour les fonctionnalités d'intelligence artificielle.

## 🚀 Démarrage rapide

```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installation des dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Modifier .env avec vos clés API

# Démarrage du serveur
python main.py
```

## 📦 Technologies utilisées

- **FastAPI** - Framework web moderne et rapide
- **OpenAI API** - Intelligence artificielle
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI
- **Python 3.11+** - Langage de programmation

## 🏗️ Structure

```
├── main.py              # Application FastAPI principale
├── requirements.txt     # Dépendances Python
├── .env.example         # Template de configuration
├── render.yaml          # Configuration Render
└── Dockerfile           # Image Docker
```

## ⚙️ Configuration

### Variables d'environnement (.env)
```env
OPENAI_API_KEY=sk-...                    # Clé API OpenAI (obligatoire)
OPENAI_API_BASE=https://api.openai.com/v1
HUGGINGFACE_API_KEY=hf_...              # Clé API HuggingFace (optionnel)
HOST=0.0.0.0
PORT=8000
```

### Modèles supportés
- **OpenAI** : gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash
- **HuggingFace** : bigcode/starcoder

## 🔌 Endpoints API

### `POST /generate`
Génération de réponses IA génériques.

### `POST /explain`
Explication détaillée du code.

### `POST /refactor`
Refactorisation du code.

### `POST /generate-code`
Génération de code basée sur une description.

### `POST /detect-bugs`
Détection de bugs potentiels.

### `POST /optimize`
Optimisation du code.

### `GET /docs`
Documentation interactive Swagger UI.

## 🔒 Sécurité

- **CORS** configuré pour les domaines autorisés
- **Validation des entrées** avec Pydantic
- **Gestion des erreurs** centralisée
- **Rate limiting** (recommandé pour la production)

## 🚀 Déploiement

### Render (recommandé)
Le fichier `render.yaml` configure automatiquement le déploiement.

### Docker
```bash
docker build -t ai-coding-assistant-backend .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=votre_clé \
  ai-coding-assistant-backend
```

### Manuel
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📊 Monitoring

### Logs
Les logs sont automatiquement générés par Uvicorn et FastAPI.

### Health Check
Endpoint `/` pour vérifier l'état du service.

### Métriques
- Temps de réponse API
- Utilisation des tokens OpenAI
- Taux d'erreur

## 🔧 Développement

### Mode debug
```bash
uvicorn main:app --reload --log-level debug
```

### Tests (à implémenter)
```bash
python -m pytest tests/
```

### Ajout d'endpoints
1. Créer le modèle Pydantic
2. Implémenter la fonction
3. Ajouter la route FastAPI
4. Documenter l'endpoint

