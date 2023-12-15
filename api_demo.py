import argparse
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from configs import VERSION
from core import BaseResponse


def create_app():
    app = FastAPI(
        title="Chat2BI API SERVER",
        version=VERSION
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    mount_app_routes(app)
    return app


def mount_app_routes(app: FastAPI):
    from core import build_tools
    from core import function_calling
    # Tag: build-tools
    app.post("/api/build_tools",
             tags=["创建工具集"],
             response_model=BaseResponse,
             summary="生成本地工具调用配置文件",
             )(build_tools)

    # function-calling
    app.post("/api/chat",
             tags=["获取工具调用结果"],
             response_model=BaseResponse,
             summary="拿到api返回内容",
             )(function_calling)


def run_api(host, port, **kwargs):
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7861)
    args = parser.parse_args()
    app = create_app()
    # mount_app_routes(app=app)
    run_api(host=args.host,
            port=args.port
            )
