from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import JSONResponse

from src.routers import likes_routes, media_routes, tweets_routes, user_routes

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(likes_routes.router)
app.include_router(media_routes.router)
app.include_router(tweets_routes.router)
app.include_router(user_routes.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5"
        "/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc) -> JSONResponse:
    """
    Обработчик исключений при ошибке в запросе,
    для вывода ошибочного результата
    :param request: запрос для эндпоинта
    :param exc: пойманное исключение
    :return: JSONResponse, для вывода корректных данных в ответе для api
    """
    return JSONResponse(
        content={
            "result": False,
            "error_type": "HTTPException",
            "error_message": exc.detail,
        },
        status_code=exc.status_code,
    )
