import pkgutil
from importlib import import_module
from importlib.metadata import metadata

import richuru
from fastapi import APIRouter, FastAPI
from loguru import logger

richuru.install()

app_metadata = metadata("mccag")

app = FastAPI(
    title="MCCAG API",
    summary=app_metadata.get("Summary", ""),
    version=app_metadata.get("Version", ""),
    license_info={"name": app_metadata.get("License", "")},
)

# Dyamically load routers

for module_info in pkgutil.iter_modules(["src/mccag/routers"]):
    logger.info(f"Loading router: {module_info.name}")
    router: APIRouter = import_module(f"mccag.routers.{module_info.name}").router
    app.include_router(router)
