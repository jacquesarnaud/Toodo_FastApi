from fastapi import FastAPI
from router.apitache_router import router_tache
from router.auth_router import router_auth


app = FastAPI()


app.include_router(router_tache)
app.include_router(router_auth)
