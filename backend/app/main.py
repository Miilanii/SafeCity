from fastapi import FastAPI
from routes import router as api_router
app = FastAPI(title='SafeCity API')
app.include_router(api_router, prefix='/api')
@app.get('/')
def root():
    return {'service':'SafeCity','status':'ok'}
