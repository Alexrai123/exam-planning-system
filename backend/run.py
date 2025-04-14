import uvicorn
import logging

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    # Run the application with debug mode enabled
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
