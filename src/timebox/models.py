from __future__ import annotations

import random
import typing

import pydantic


class DistributionInfo(pydantic.BaseModel):
    kind: str
    description: str
    arguments: dict[str, str]


class _BaseDistribution(pydantic.BaseModel):
    """Base for random distribution types"""

    kind: typing.ClassVar[str] = "_base"
    scale: float = 1.0
    drift: float = 0.0

    @classmethod
    def describe(cls) -> DistributionInfo:
        return {
            "kind": cls.kind,
            "description": cls.__doc__,
            "arguments": {
                "scale": "float, default 1.0",
                "drift": "float, default 0.0",
            },
        }


class LogNormVariateDistribution(_BaseDistribution):
    __doc__ = random.lognormvariate.__doc__
    kind: typing.ClassVar[str] = "lognormvariate"
    mu: float
    sigma: float

    @classmethod
    def describe(cls) -> DistributionInfo:
        base = super().describe()
        return base | {
            "arguments": base["arguments"]
            | {
                "mu": "float",
                "sigma": "float > 0",
            }
        }


class NormVariateDistribution(_BaseDistribution):
    __doc__ = random.normalvariate.__doc__
    kind: typing.ClassVar[str] = "normalvariate"
    mu: float
    sigma: float

    @classmethod
    def describe(cls) -> DistributionInfo:
        base = super().describe()
        return base | {
            "arguments": base["arguments"]
            | {
                "mu": "float",
                "sigma": "float",
            }
        }


class ParetoVariateDistribution(_BaseDistribution):
    __doc__ = random.paretovariate.__doc__
    kind: typing.ClassVar[str] = "paretovariate"
    alpha: float

    @classmethod
    def describe(cls) -> DistributionInfo:
        base = super().describe()
        return base | {
            "arguments": base["arguments"]
            | {
                "alpha": "float",
            }
        }


class TriangularDistribution(_BaseDistribution):
    __doc__ = random.triangular.__doc__
    kind: typing.ClassVar[str] = "triangular"
    low: float
    high: float
    mode: float | None = None

    @classmethod
    def describe(cls) -> DistributionInfo:
        base = super().describe()
        return base | {
            "arguments": base["arguments"]
            | {
                "low": "float",
                "high": "float",
                "mode": "float | None, default None",
            }
        }


class WeibullVariateDistribution(_BaseDistribution):
    __doc__ = random.weibullvariate.__doc__
    kind: typing.ClassVar[str] = "weibullvariate"
    alpha: float

    @classmethod
    def describe(cls) -> DistributionInfo:
        base = super().describe()
        return base | {
            "arguments": base["arguments"]
            | {
                "alpha": "float",
                "beta": "float",
            }
        }


Distributions = (
    LogNormVariateDistribution
    | NormVariateDistribution
    | TriangularDistribution
    | ParetoVariateDistribution
    | WeibullVariateDistribution
)


class DistributionQuery(pydantic.BaseModel):
    kind: str
    arguments: dict[str, typing.Any] | None = None


class DatapointQuery(pydantic.BaseModel):
    name: str
    distribution: DistributionQuery


class TimeboxQuery(pydantic.BaseModel):
    frequency: float = 10.0
    points: list[DatapointQuery]


class TimeboxRecord(pydantic.BaseModel):
    timestamp: str  # ISO format
    points: dict[str, float]
