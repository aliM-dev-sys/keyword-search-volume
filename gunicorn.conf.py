# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes - optimized for shared server (2 vCPU, 4GB RAM)
workers = 2  # Reduced from cpu_count() * 2 + 1 to prevent resource conflicts
worker_class = "sync"
worker_connections = 500  # Reduced from 1000
timeout = 60  # Increased to handle Google Trends API delays
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 500  # Reduced for shared server
max_requests_jitter = 25

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "keyword-search-volume-api"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None
