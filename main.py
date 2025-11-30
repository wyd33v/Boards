# TODO:
"""
1 read about docker networks again.
2. Add test coverage for cache_service.py (read todo).

* inspect MQTT as a message broker
3. Add message broker service in docker-compose (same way as cache service is added)

4. Add Broker service in the app (same way as cache_service)

5. Write simple worker which uses message broker event and puts some result in cache 

"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=4)
