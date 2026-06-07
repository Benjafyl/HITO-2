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

Resultados locales finales recomendados para el informe:

| Escenario | Requests /flights | Avg /flights | P95 /flights | RPS /flights | Fallos /flights |
| --- | ---: | ---: | ---: | ---: | ---: |
| Before sin cache final | 401 | 97902.61 ms | 268000 ms | 1.46 | 255 |
| After Redis final | 26220 | 5649.99 ms | 6700 ms | 87.50 | 0 |

Lectura tecnica final: bajo 1000 usuarios concurrentes, el escenario sin cache
presento saturacion severa, baja tasa de procesamiento y fallos. Con Redis
activado, la API mantuvo 0 fallos, mayor throughput y una reduccion relevante en
latencia para `GET /flights`.

Resultados locales anteriores disponibles en `results/`:

| Escenario | Requests /flights | Avg /flights | P95 /flights | RPS /flights | Fallos /flights |
| --- | ---: | ---: | ---: | ---: | ---: |
| Before sin cache | 21928 | 7178.68 ms | 9300 ms | 73.17 | 0 |
| After Redis | 19476 | 8218.20 ms | 11000 ms | 64.98 | 0 |

Lectura tecnica de la corrida anterior: en esa ejecucion local no se observo una
reduccion de latencia en el CSV de Locust, aunque si se verifico funcionamiento
de Redis, cache hits, cache misses y 0 fallos. Se conserva como evidencia
historica, pero para el informe se recomienda usar los archivos `before-final_*`
y `after-redis-final_*`.

## Capturas requeridas

Guardar capturas exportadas desde Grafana en `results/` con nombres claros, por
ejemplo:

- `results/grafana-before.png`
- `results/grafana-after-redis.png`

No editar manualmente CSV ni capturas.

Las capturas disponibles estan descritas en `results/evidence-index.md`.
