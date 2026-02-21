from fastapi import APIRouter
from ..schemas import LogCreate
from ..storage import add_log, get_logs, clear_logs

router = APIRouter()


@router.post("/logs")
def receive_log(log: LogCreate):
    log_dict = log.model_dump()
    add_log(log_dict)

    return {
        "status": "log received",
        "device_id": log.device_id
    }


@router.get("/logs")
def view_logs():
    return get_logs()


@router.delete("/logs")
def delete_logs():
    clear_logs()
    return {"status": "logs cleared"}