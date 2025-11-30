import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models.processes import ProcessStatus
from services import CacheService, cache_service

router = APIRouter(prefix="/processes", tags=["processes"])


def create_req_id():
    return uuid.uuid4()

@router.get("")
def get_process_status(req_id: str, cache: CacheService = Depends(cache_service)):
    try:
        value = cache.get_process(req_id)
        return value
    except KeyError:
        # log error
        return JSONResponse(status_code=404, content={"status": ProcessStatus.FAILURE})
