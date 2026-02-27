# `timebox`:  Simulate timeseries for one or more data points

FastAPI app, no persistence

## `POST /api/vi/timebox/distributions`

Return a list of supported distributions, with descriptions and arguments.

## `POST /api/vi/timebox`

Streams emulated timeseries for requested data points.

Request body (spelled here as YAML, but submitted as JSON):

```
frequency: <float, seconds, default 10s>
points:
  - name: "foo"
    kind: "gauss":
    arguments:
      mu: <float>
      sigma: <float>
  - name: "bar"
    kind: "paretovariate"
      alpha: <float>
  - name: "baz"
    kind: "expovariate"
      lambd: <float>
  - name: "bam":
    kind: "gammavariate"
      alpha: <float >0)
      beta: <float >0)
  - name: "qux"
    kind: "betavariate"
      alpha: <float >0)
      beta: <float >0)
  - name: "spam"
    kind: "lognormvariate"
      mu: <float>
      sigma: <float >0>
  - name: "frob"
    kind: "normvariate"
      mu: <float>
      sigma: <float>
  - name: "nadz" 
    kind: "triangular"
      low: <float>
      high: <float>
      mode: <float>
  - name: "karf"
    kind: "vonmisesvariate"
      mu: <float>
      kappa: <float>
      scale: <float>
  - name: "xyph"
    kind: "weibullvariate"
      alpha: float
      beta: float
```

SSE response records:
```
{"timestamp": "2026-02-26T23:45:01Z", "foo": 12.345, "bar": 6.789, ....}
```
