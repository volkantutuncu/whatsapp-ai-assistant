# WhatsApp AI Assistant Backend

## Local setup

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Health endpoint: `http://127.0.0.1:8000/health`
