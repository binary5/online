import os
os.environ.setdefault("DJANGO_ENVIRONMENT", "development")

import uvicorn
from online import asgi
if __name__ == "__main__":
    uvicorn.run(asgi.application, host="127.0.0.1", port=8000)
