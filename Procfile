init_db: flask db init
migrate_db: flask db migrate -m "Your migration message"
upgrade_db: flask db upgrade
web: gunicorn --worker-tmp-dir /dev/shm --config gunicorn_config.py app:app