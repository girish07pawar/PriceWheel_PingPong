from fastapi import FastAPI
import uvicorn
import httpx
import asyncio
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pong-service")

app = FastAPI()

# URL of your main application - update this with your actual deployed main project URL
MAIN_APP_URL = "https://backup-predectionmodel25-rjvo.onrender.com"

@app.get("/")
def read_root():
    return {"status": "Pong service is running"}

@app.get("/pong")
def pong():
    logger.info("Received pong request")
    return {"message": "Pong received", "timestamp": str(datetime.now())}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "pong", "timestamp": str(datetime.now())}

async def keep_alive_task():
    """Background task that pings the main app every 5 minutes"""
    while True:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Ping the main app
                logger.info(f"Sending request to main app: {MAIN_APP_URL}")
                
                try:
                    response = await client.get(MAIN_APP_URL)
                    logger.info(f"Received response from main app: {response.status_code}")
                except Exception as e:
                    logger.error(f"Failed to ping main app: {e}")
                
                # Skip self-pinging as it might be causing issues
                logger.info("Skipping self-ping as it might be causing connection issues")
                
        except Exception as e:
            logger.error(f"Error in keep-alive task: {e}")
        
        # Wait for 5 minutes before the next ping cycle
        logger.info("Waiting 5 minutes before next ping cycle")
        await asyncio.sleep(300)

@app.on_event("startup")
async def startup_event():
    """Start the background keep-alive task when the app starts"""
    logger.info("Starting pong service background task")
    asyncio.create_task(keep_alive_task())

if __name__ == "__main__":
    uvicorn.run("PongServices:app", host="0.0.0.0", port=8000)