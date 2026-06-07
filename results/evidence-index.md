# Indice de evidencias

Esta carpeta contiene evidencia generada localmente para el Hito 3. Los CSV son
salidas directas de Locust y las imagenes son capturas de validacion funcional y
observabilidad.

## Capturas incluidas

| Archivo | Evidencia |
| --- | --- |
| `screenshots/01-docker-compose-ps.jpeg` | Servicios Docker levantados: backend, frontend, db, redis, Prometheus, Grafana, cAdvisor y Locust |
| `screenshots/02-endpoints-api.jpeg` | Prueba parcial de endpoints (`health`, `flights`, `routes`) |
| `screenshots/02b-endpoints-api-completo.jpeg` | Prueba completa de endpoints (`health`, `flights`, `routes`, `aircraft`) |
| `screenshots/03-redis-ping.jpeg` | Redis responde `PONG` |
| `screenshots/04-redis-cache-keys.jpeg` | Redis contiene claves `aircraft:all`, `flights:all`, `routes:all` |
| `screenshots/05-backend-metrics-requests.jpeg` | Metricas HTTP del backend |
| `screenshots/06-backend-metrics-latency-flights.jpeg` | Histograma de latencia para `/flights` |
| `screenshots/07-backend-metrics-latency-counts.jpeg` | Histogramas de latencia para endpoints de catalogo |
| `screenshots/08-backend-metrics-cache.jpeg` | Metricas `cache_hits_total` y `cache_misses_total` |
| `screenshots/09-prometheus-targets.jpeg` | Targets Prometheus en estado `UP` |
| `screenshots/10-grafana-before-dashboard.jpeg` | Dashboard Grafana en escenario before |
| `screenshots/11-grafana-before-cache.jpeg` | Cache hit ratio y hits/misses en escenario before |
| `screenshots/12-grafana-after-dashboard.jpeg` | Dashboard Grafana en escenario after Redis |
| `screenshots/13-grafana-after-cache.jpeg` | Cache hit ratio y hits/misses en escenario after Redis |
| `screenshots/14-frontend.jpeg` | Frontend React funcionando en `http://localhost:3002` |
| `screenshots/15-api-docs.jpeg` | Swagger/API Docs funcionando en `http://localhost:8001/docs` |
| `screenshots/16-grafana-cpu-memory-updated.jpeg` | Paneles Grafana de CPU y memoria con datos desde cAdvisor |

## CSV de Locust incluidos

| Archivo | Escenario |
| --- | --- |
| `before_stats.csv` | Prueba de carga sin cache |
| `before_stats_history.csv` | Historial temporal sin cache |
| `before_failures.csv` | Fallos sin cache |
| `before_exceptions.csv` | Excepciones sin cache |
| `after-redis_stats.csv` | Prueba de carga con Redis |
| `after-redis_stats_history.csv` | Historial temporal con Redis |
| `after-redis_failures.csv` | Fallos con Redis |
| `after-redis_exceptions.csv` | Excepciones con Redis |
| `before-final_stats.csv` | Prueba final de carga sin cache |
| `before-final_stats_history.csv` | Historial temporal final sin cache |
| `before-final_failures.csv` | Fallos finales sin cache |
| `before-final_exceptions.csv` | Excepciones finales sin cache |
| `after-redis-final_stats.csv` | Prueba final de carga con Redis |
| `after-redis-final_stats_history.csv` | Historial temporal final con Redis |
| `after-redis-final_failures.csv` | Fallos finales con Redis |
| `after-redis-final_exceptions.csv` | Excepciones finales con Redis |

## Evidencias recomendadas pendientes

- Captura de `docker compose ps` con todos los servicios arriba.
- Captura del frontend en `http://localhost:3002`.
- Captura de Swagger/API Docs en `http://localhost:8001/docs`.
- Captura del resumen final de Locust para before y after.

Nota: en Docker Desktop/WSL, cAdvisor puede exponer metricas con etiqueta `id`
en vez de nombres de servicios Docker. El dashboard fue ajustado para mostrar
CPU y memoria usando las series disponibles por `id`.
