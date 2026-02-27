import json

import pandas as pd
import requests

TIMEBOX_URL = "http://localhost:8899/api/v1/timebox"
TIMEBOX_QUERY = {
    "frequency": 1.0,
    "points": [
        {
            "name": "foo",
            "distribution": {
                "kind": "lognormvariate",
                "arguments": {"mu": 1.0, "sigma": 0.5},
            },
        },
        {
            "name": "bar",
            "distribution": {
                "kind": "normalvariate",
                "arguments": {"mu": 0.0, "sigma": 10.0},
            },
        },
    ],
}
WINDOW_SIZE = 10


def main():
    dp_columns = [point["name"] for point in TIMEBOX_QUERY["points"]]
    records = pd.DataFrame(
        {
            "timestamp": [pd.Timestamp.now("UTC")],
        }
        | {column: None for column in dp_columns}
    )

    response = requests.post(
        url=TIMEBOX_URL,
        json=TIMEBOX_QUERY,
        stream=True,
    )
    if response.encoding is None:
        response.encoding = "utf-8"

    for line in response.iter_lines(decode_unicode=True):
        if line:
            record = json.loads(line)

            row = (pd.Timestamp(record["timestamp"]),) + tuple(
                record[dp_col] for dp_col in dp_columns
            )

            if len(records) > WINDOW_SIZE:
                print()
                records = records.shift(-1)
                records.iloc[-1] = row

                for dp_col in dp_columns:
                    value = records.iloc[-1][dp_col]
                    mean = records.iloc[:-1][dp_col].mean()
                    sigma = records.iloc[:-1][dp_col].std()
                    delta = abs(value - mean)

                    if delta > sigma * 1.5:
                        print(f"{row[0]}: column: {dp_col} > 1.5 *sigma")

            else:
                count = len(records)
                records.loc[count] = row
                print(f"Filling window: [{count}/{WINDOW_SIZE}]")


if __name__ == "__main__":
    main()
