"""
Gunicorn Config
"""

import os
import multiprocessing

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2
accesslog = "-"
