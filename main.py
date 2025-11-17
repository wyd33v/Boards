# TODO:
"""
* read about docker-compose networks.

3. Add background tasks

--------------------------
4. Message brokers



"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=4)
