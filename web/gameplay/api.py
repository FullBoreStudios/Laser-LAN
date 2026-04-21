from ninja import Router

router = Router(tags=["gameplay"])


@router.get("/meta")
def gameplay_meta(request):
    return {
        "mode": "bomb_defusal",
        "notes": [
            "Phone is treated as the round-state authority.",
            "Round snapshots and event logs are stored separately.",
        ],
    }
