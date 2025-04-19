from fastapi import FastAPI
import uvicorn
import httpx
import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pong-service")

app = FastAPI()

# URL of your main application - update this with your actual deployed main project URL
PING_URL = "https://backup-predectionmodel25.onrender.com/"

@app.get("/")
def read_root():
    return {"status": "Pong service is running"}

@app.get("/pong")
def pong():
    return {"message": "Pong received", "timestamp": str(datetime.now())}

async def pong_ping_task():
    """Background task that pings the main app every 2 minutes"""
    while True:
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Sending request to {PING_URL}")
                response = await client.get(PING_URL)
                logger.info(f"Received response: {response.status_code}")
        except Exception as e:
            logger.error(f"Error pinging main app: {e}")
        
        # Wait for 2 minutes before the next ping
        await asyncio.sleep(120)

@app.on_event("startup")
async def startup_event():
    """Start the background pong task when the app starts"""
    asyncio.create_task(pong_ping_task())

if __name__ == "__main__":
    uvicorn.run("PongServices:app", host="0.0.0.0", port=8000)