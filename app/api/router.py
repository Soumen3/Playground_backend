from api.v1.routes.playground import router as playground_router

def include_router(app):
    app.include_router(playground_router)
    