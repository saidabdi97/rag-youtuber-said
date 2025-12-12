import sys
from pathlib import Path

import azure.functions as func

# ➜ Lägg till projektroten i PYTHONPATH
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# ➜ Importera FastAPI-appen från src/api/main.py
from src.api import main as api


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="{*route}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def fastapi_proxy(
    req: func.HttpRequest, context: func.Context
) -> func.HttpResponse:
    return await func.AsgiMiddleware(api.app).handle_async(req, context)
