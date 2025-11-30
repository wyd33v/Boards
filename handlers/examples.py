from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from services import CacheService, cache_service

router = APIRouter(prefix="/examples", tags=["examples"])


@router.get("/cache")
def set_cache_key_example(key: str, cache: CacheService = Depends(cache_service)):
    try:
        value = cache.get_value(key)
        return {"Hello": "World", "value": value}
    except KeyError:
        # log error
        err = "value not found"
        return JSONResponse(status_code=404, content={"message": err})


@router.post("/cache")
def get_cache_key_example(key: str, value, exp: int, cache: CacheService = Depends(cache_service)):
    cache.set_value(key, value, exp)
    return {"status": "ok"}
