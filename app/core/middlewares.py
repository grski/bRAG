from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "HEAD", "OPTIONS", "DELETE"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Set-Cookie",
        ],
    )
    return app


# def add_sentry_middleware(app: FastAPI) -> FastAPI:
#     if settings.SENTRY_DSN:  # pragma: no cover
#         sentry_sdk.init(
#             dsn=settings.SENTRY_DSN,
#             environment=settings.ENVIRONMENT,
#             send_default_pii=False,
#             traces_sample_rate=0.3,
#             profiles_sample_rate=0.3,
#         )
#         app.add_middleware(SentryAsgiMiddleware)
#     return app


MIDDLEWARES = (
    add_cors_middleware,
    # add_sentry_middleware,
)


def apply_middlewares(app: FastAPI) -> FastAPI:
    for middleware in MIDDLEWARES:
        app = middleware(app)
    return app
