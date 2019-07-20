web: gunicorn app:app --timeout 30 --workers 3 
worker: rq worker -u $REDIS_URL app


