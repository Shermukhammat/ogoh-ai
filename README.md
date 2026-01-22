# ogoh-ai
Project for national AI hackathon Uzbekistan.

## Quick start (.venv example)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requairments.txt
```

## Environment variables (.env example)
```env
GEMINI_API_KEY=""
DEBUG="True"

API_HASH=""
API_ID=""
PHONE_NUM="+998123456789"
BOT_TOKEN=""

REST_API_TOKEN=""
```

## Run
```bash
python manage.py migrate
python manage.py runserver
```
