from ninja import NinjaAPI

from gameplay.api import router as gameplay_router

api = NinjaAPI(
    title="Laser LAN API",
    version="0.1.0",
    description="Backend API for match, round, and device-driven gameplay state.",
)


@api.get("/health", tags=["system"])
def health(request):
    return {"status": "ok"}


api.add_router("/gameplay/", gameplay_router)
