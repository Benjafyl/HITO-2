import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests by method, endpoint and status code.",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds by method and endpoint.",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)

CACHE_HITS_TOTAL = Counter(
    "cache_hits_total",
    "Total cache hits by endpoint.",
    ["endpoint"],
)

CACHE_MISSES_TOTAL = Counter(
    "cache_misses_total",
    "Total cache misses by endpoint.",
    ["endpoint"],
)


async def metrics_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.perf_counter()
    status_code = "500"
    endpoint = request.url.path

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        route = request.scope.get("route")
        endpoint = getattr(route, "path", endpoint)
        return response
    finally:
        elapsed = time.perf_counter() - start
        REQUESTS_TOTAL.labels(request.method, endpoint, status_code).inc()
        REQUEST_LATENCY_SECONDS.labels(request.method, endpoint).observe(elapsed)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
