from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from ..cache import FLIGHTS_CACHE_KEY, FLIGHTS_TTL_SECONDS, get_cached_json, set_cached_json
from ..database import get_db
from ..metrics import CACHE_HITS_TOTAL, CACHE_MISSES_TOTAL
from ..models import Aircraft, Booking, Flight
from ..schemas import FlightOut

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("", response_model=list[FlightOut])
def get_flights(db: Session = Depends(get_db)):
    """
    Endpoint crítico del sistema base.

    Realiza un JOIN entre flights, routes, aircraft y una subconsulta sobre
    bookings para calcular asientos disponibles. Bajo alta concurrencia esta
    consulta se convierte en el principal cuello de botella del sistema.

    NOTA PARA EL ALUMNO: este endpoint NO usa caché. Mide la latencia en su
    estado actual con Locust y luego implementa Redis para reducirla.
    """
    cached = get_cached_json(FLIGHTS_CACHE_KEY)
    if cached is not None:
        CACHE_HITS_TOTAL.labels("/flights").inc()
        return cached

    CACHE_MISSES_TOTAL.labels("/flights").inc()

    # Subconsulta: reservas confirmadas por vuelo
    booked_subq = (
        select(
            Booking.flight_id,
            func.count(Booking.id).label("booked_count"),
        )
        .where(Booking.status == "confirmed")
        .group_by(Booking.flight_id)
        .subquery()
    )

    rows = (
        db.query(Flight, func.coalesce(booked_subq.c.booked_count, 0).label("booked"))
        .options(joinedload(Flight.route), joinedload(Flight.aircraft))
        .outerjoin(booked_subq, Flight.id == booked_subq.c.flight_id)
        .filter(Flight.status != "cancelled")
        .order_by(Flight.departure_date)
        .all()
    )

    flights = [
        FlightOut(
            id=flight.id,
            departure_date=flight.departure_date,
            arrival_date=flight.arrival_date,
            price=flight.price,
            status=flight.status,
            available_seats=max(flight.aircraft.capacity - int(booked), 0),
            route=flight.route,
            aircraft=flight.aircraft,
        )
        for flight, booked in rows
    ]

    payload = jsonable_encoder(flights)
    set_cached_json(FLIGHTS_CACHE_KEY, payload, FLIGHTS_TTL_SECONDS)
    return payload
