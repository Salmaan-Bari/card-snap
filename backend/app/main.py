from fastapi import FastAPI

app = FastAPI(title="CardSnap API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "CardSnap backend is running."}


@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": "v1"}
