#!/usr/bin/env python3


from sys import argv, exit
from importlib import import_module
from importlib.metadata import version

DEPENDENCIES = {
    "pandas": "Data manipulation",
    # "numpy": "Numerical computation",
    "requests": "Network access",
    "matplotlib": "Visualization",
}


def validate_dependencies() -> None:
    has_missing = False
    for package, description in DEPENDENCIES.items():
        try:
            import_module(package)
            ver = version(package)
            print(f"[OK] {package} ({ver}) - {description} ready")
        except ImportError:
            has_missing = True
            print(f"[MISSING] {package} - {description}")

    if has_missing:
        raise ImportError(
            "\n".join(
                [
                    "",
                    "Missing packages should be installed",
                    "",
                    "For pip, type:",
                    "-----------------",
                    "pip install -r ./requirements.txt",
                    f"python3 {argv[0]}",
                    "",
                    "For Poetry, type:",
                    "-----------------",
                    "poetry install",
                    # "poetry install -P ex1",
                    # "poetry install -C ex1",
                    f"poetry run python {argv[0]}",
                ]
            )
        )


def request_data() -> dict[str, list[float]]:
    from requests import get
    from requests.exceptions import (
        JSONDecodeError,
        RequestException,
    )

    url = "https://api.open-meteo.com/v1/forecast"
    params: dict[str, float | str | list[str]] = {
        # "latitude": 40.7925694444,
        # "longitude": 29.5107055556,
        "latitude": 40.7925,
        "longitude": 29.5107,
        "daily": [
            "apparent_temperature_min",
            "apparent_temperature_max",
        ],
        "past_days": 92,
        "timezone": "auto",
    }

    try:
        response = get(url, params=params)
        data = response.json()

        return data["daily"]
    except JSONDecodeError as e:
        raise RequestException("The server returned invalid JSON: " + str(e))
    except KeyError as e:
        raise RequestException("Cannot find the key: " + str(e))
    except RequestException as e:
        raise RequestException("Request failed: " + str(e))


def main() -> None:
    print()
    print("LOADING STATUS: Loading programs...")

    print()
    print("Checking dependencies:")
    try:
        validate_dependencies()
    except ImportError as e:
        exit(str(e))

    print()
    print("Requesting data...")
    try:
        data = request_data()
    except IOError as e:
        exit(str(e))

    # import numpy as np
    from pandas import DataFrame, to_datetime
    from matplotlib import pyplot as plot

    data_frame = DataFrame(data)

    print("Analyzing Matrix data...")
    data_frame = data_frame.dropna(
        subset=["apparent_temperature_min", "apparent_temperature_max"]
    )
    data_frame["time"] = to_datetime(data_frame["time"])

    x = data_frame["time"]
    y1 = data_frame["apparent_temperature_min"]
    y2 = data_frame["apparent_temperature_max"]

    print(f"Processing {len(x)} data points...")

    figure, axes = plot.subplots(figsize=(12, 8), dpi=120)
    axes.fill_between(
        x=x, y1=y1, y2=y2, alpha=0.3, color="orange", label="temperature range"
    )
    axes.plot(
        x,
        (y1 + y2) / 2,
        color="red",
        linewidth=3,
        marker="o",
        markersize=5,
        label="average apparent temperature",
    )
    axes.set(ylim=(min(y1.min(), y2.min()) - 2, max(y1.max(), y2.max()) + 2))

    axes.set_title(
        "42 Kocaeli | Apparent Temperature Over Time",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )
    axes.set_xlabel("Date")
    axes.set_ylabel("Temperature (°C)")
    axes.legend()
    axes.grid()
    # axes.spines["top"].set_visible(False)
    # axes.spines["right"].set_visible(False)
    figure.autofmt_xdate()

    print("Generating visualization...")
    save_file = "matrix_analysis.png"
    plot.savefig(save_file)
    plot.show()

    print()
    print("Analysis complete!")
    print("Results saved to:", save_file)


if __name__ == "__main__":
    main()
