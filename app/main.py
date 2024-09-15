from fastapi import Depends, FastAPI, HTTPException, Request
from routers import files
from db.database import engine
from models import file
import json
import os

# Create the database tables
file.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(files.router, prefix="/V1")

# Load configuration from config.json
# dir_path = os.path.dirname(os.path.realpath(__file__))
# config_path = os.path.join(dir_path, "config.json")
# with open(config_path, "r") as config_file:
#     config = json.load(config_file)

# @app.middleware("http")
# async def check_access(request: Request, call_next):
#     client_ip = request.client.host
#     pre_shared_key = request.headers.get("Pre-Shared-Key")

#     if not any(ip["ip"] == client_ip and ip["pre_shared_key"] == pre_shared_key for ip in config["whitelist_ips"]):
#         raise HTTPException(status_code=403, detail="Access Denied: IP or pre-shared key not allowed")

#     response = await call_next(request)
#     return response

@app.get("/")
async def root():
    return {"message": "Hello oceanbridge-poc"}


#need access control allow headers / methods





