"""Stream faux timeseries data over an API endpoint

Usage:

$ uvicorn --port #### "timebox.server.app"
"""

from __future__ import annotations

import asyncio
import datetime
import functools
import json
import random
import typing

import fastapi
import uvicorn
from fastapi import responses

from timebox import models

app = fastapi.FastAPI()
router = fastapi.APIRouter()


@router.get(
    "/ok", response_class=responses.PlainTextResponse, tags=["process"]
)
async def health_check() -> str:
    """Check that the server is up and running"""
    return "OK"


@router.get("/v1/timebox/distributions")
async def get_timebox_distributions(
    request: fastapi.Request,
) -> dict[typing.Literal["distributions"], list[models.DistributionInfo]]:
    """Get available random distributions"""
    return {
        "distributions": [
            klass.describe() for klass in models.Distributions.__args__
        ],
    }


@router.post("/v1/timebox/distribution")
async def post_timebox_distribution(
    query: models.DistributionQuery,
) -> float:
    """Compute a value using the given distribution"""
    return getattr(random, query.kind)(**query.arguments)


@router.post("/v1/timebox")
async def post_timebox(
    query: models.TimeboxQuery,
) -> responses.StreamingResponse:
    """Compute a value using the given distribution"""

    distributions = {
        point.name: functools.partial(
            getattr(random, point.distribution.kind),
            **(point.distribution.arguments | {}),
        )
        for point in query.points
    }

    async def generate_points():
        while True:
            now = datetime.datetime.now(datetime.UTC)
            record = {
                "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            } | {key: value() for key, value in distributions.items()}
            yield f"{json.dumps(record)}\n"
            await asyncio.sleep(query.frequency)

    return responses.StreamingResponse(
        generate_points(),
    )


app.include_router(router, prefix="/api")


if __name__ == "__main__":  # pragma:  NO COVER
    uvicorn.run(app, port=8899)
