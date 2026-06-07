# Resultados de pruebas

Este documento define como generar y registrar la evidencia. No contiene
metricas fabricadas.

## Escenarios obligatorios

| Escenario | Cache | Usuarios | Spawn rate | Duracion | CSV |
| --- | --- | ---: | ---: | --- | --- |
| Before | Desactivada | 1000 | 50/s | 5m | `results/before_*` |
| After Redis | Activada | 1000 | 50/s | 5m | `results/after-redis_*` |

## Comandos PowerShell

Before:

```powershell
$env:CACHE_ENABLED='false'
docker compose up --build
docker compose run --rm locust locust -f locustfile.py --host=http://backend:8000 --users 1000 --spawn-rate 50 --run-time 5m --headless --csv=results/before
```

After Redis:

```powershell
$env:CACHE_ENABLED='true'
docker compose up --build
docker compose run --rm locust locust -f locustfile.py --host=http://backend:8000 --users 1000 --spawn-rate 50 --run-time 5m --headless --csv=results/after-redis
```

## Prueba de humo

```bash
docker compose run --rm locust locust -f locustfile.py --host=http://backend:8000 --users 10 --spawn-rate 5 --run-time 30s --headless --csv=results/smoke
```

## Metricas a extraer

Desde Locust:

- Average response time para `/flights`.
- P95 para `/flights`.
- Requests por segundo.
- Fallos y porcentaje de error.

Desde Grafana:

- Latencia promedio `/flights`.
- Latencia P95 `/flights`.
- Cache Hit Ratio.
- CPU backend/db/redis.
- Memoria backend/db/redis.

## Tabla para completar

| Escenario | Avg /flights | P95 /flights | RPS | Fallos | Cache Hit Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Before | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| After Redis | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Capturas requeridas

Guardar capturas exportadas desde Grafana en `results/` con nombres claros, por
ejemplo:

- `results/grafana-before.png`
- `results/grafana-after-redis.png`

No editar manualmente CSV ni capturas.
