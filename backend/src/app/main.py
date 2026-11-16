from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/')
def root():
    return { 'message': 'testing food delivery app from main.py'}


if __name__ == '__main__':
    uvicorn.run(__name__ + ":app", host='0.0.0.0', port=8000, reload=True)
