import multiprocessing
import uvicorn

wsgi_app = "app:application"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600
loglevel = "debug"
preload_app = True
worker_class = 'uvicorn.worksers.UvicornWorker'