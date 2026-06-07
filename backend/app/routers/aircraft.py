from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..cache import AIRCRAFT_CACHE_KEY, CATALOG_TTL_SECONDS, get_cached_json, set_cached_json
from ..database import get_db
from ..metrics import CACHE_HITS_TOTAL, CACHE_MISSES_TOTAL
from ..models import Aircraft
from ..schemas import AircraftOut

router = APIRouter(prefix="/aircraft", tags=["aircraft"])


@router.get("", response_model=list[AircraftOut])
def get_aircraft(db: Session = Depends(get_db)):
    cached = get_cached_json(AIRCRAFT_CACHE_KEY)
    if cached is not None:
        CACHE_HITS_TOTAL.labels("/aircraft").inc()
        return cached

    CACHE_MISSES_TOTAL.labels("/aircraft").inc()
    aircraft = db.query(Aircraft).order_by(Aircraft.id).all()
    payload = [AircraftOut.model_validate(item).model_dump(mode="json") for item in aircraft]
    set_cached_json(AIRCRAFT_CACHE_KEY, payload, CATALOG_TTL_SECONDS)
    return payload
