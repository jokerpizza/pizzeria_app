from fastapi import APIRouter, Depends
from .. import schemas, crud

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/", response_model=schemas.SettingsOut)
def get_settings():
    return {"fc_threshold": crud.get_fc_threshold()}

# For MVP we just accept value and set env in memory (not persistent). In production use DB.
import os
@router.put("/", response_model=schemas.SettingsOut)
def set_settings(data:schemas.SettingsIn):
    os.environ["FC_THRESHOLD"]=str(data.fc_threshold)
    return {"fc_threshold": data.fc_threshold}
