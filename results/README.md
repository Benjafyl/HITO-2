# Resultados de pruebas de carga

Esta carpeta queda versionada para centralizar evidencia del hito.

Los CSV y capturas se generan ejecutando Locust y Grafana localmente. No se incluyen
metricas fabricadas ni archivos editados manualmente.

Comandos principales:

```bash
docker compose run --rm locust locust -f locustfile.py --host=http://backend:8000 --users 1000 --spawn-rate 50 --run-time 5m --headless --csv=results/before
docker compose run --rm locust locust -f locustfile.py --host=http://backend:8000 --users 1000 --spawn-rate 50 --run-time 5m --headless --csv=results/after-redis
```
