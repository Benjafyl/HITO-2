from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..cache import CATALOG_TTL_SECONDS, ROUTES_CACHE_KEY, get_cached_json, set_cached_json
from ..database import get_db
from ..metrics import CACHE_HITS_TOTAL, CACHE_MISSES_TOTAL
from ..models import Route
from ..schemas import RouteOut

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("", response_model=list[RouteOut])
def get_routes(db: Session = Depends(get_db)):
    cached = get_cached_json(ROUTES_CACHE_KEY)
    if cached is not None:
        CACHE_HITS_TOTAL.labels("/routes").inc()
        return cached

    CACHE_MISSES_TOTAL.labels("/routes").inc()
    routes = db.query(Route).order_by(Route.id).all()
    payload = [RouteOut.model_validate(route).model_dump(mode="json") for route in routes]
    set_cached_json(ROUTES_CACHE_KEY, payload, CATALOG_TTL_SECONDS)
    return payload
