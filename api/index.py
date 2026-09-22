import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈을 정상적으로 import
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

# Vercel Serverless 요청 경로 정규화 미들웨어 (404 방지)
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        # Vercel이 /api/index.py 또는 /api 형태로 rewrite했을 때 원래 URL로 복원
        for prefix in ["/api/index.py", "/api/index", "/api"]:
            if path == prefix:
                environ["PATH_INFO"] = "/"
                break
            elif path.startswith(prefix + "/"):
                environ["PATH_INFO"] = path[len(prefix):]
                break
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
