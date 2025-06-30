from fastapi import FastAPI
from routes import listings, mortgage, email, agents

app = FastAPI()

app.include_router(listings.router)
app.include_router(mortgage.router)
app.include_router(email.router)
app.include_router(agents.router)





@app.get("/")
def root():
    return {"message": "FastAPI Real Estate API running"}
