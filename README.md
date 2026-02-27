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

## `timebox.server`

```bash
$ uvicorn --port 8899 "timebox.server:app"
INFO:     Uvicorn running on http://127.0.0.1:8899 (Press CTRL+C to quit)
INFO:     Started reloader process [1255767] using WatchFiles
INFO:     Started server process [1255769]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## `timebox.client`

```bash
$ python -m timebox.client
Filling window: [1/10]
Filling window: [2/10]
Filling window: [3/10]
Filling window: [4/10]
Filling window: [5/10]
Filling window: [6/10]
Filling window: [7/10]
Filling window: [8/10]
Filling window: [9/10]
Filling window: [10/10]

2026-02-27 02:22:16+00:00: column: foo > 1.5 *sigma
2026-02-27 02:22:16+00:00: column: bar > 1.5 *sigma

2026-02-27 02:22:17+00:00: column: bar > 1.5 *sigma


2026-02-27 02:22:19+00:00: column: foo > 1.5 *sigma
^CTraceback (most recent call last):
```
