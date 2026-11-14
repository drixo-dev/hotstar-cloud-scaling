import time
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'status': 'Stream available'}

@app.get('/health')
def health():
    return {'ok' : True}

@app.get('/work')
def work(n: int = 250000):
    start = time.perf_counter()
    x = 0
    for i in range(n):
        x += i * i
    ms = round((time.perf_counter() - start) * 1000, 1)
    return {'status': 'Stream available', 'n': n, 'ms': ms}