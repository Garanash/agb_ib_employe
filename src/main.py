import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    return {'status_code': 200}

if __name__ == '__main__':
    uvicorn.run("main:app", port=7890)