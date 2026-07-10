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


def check_dependencies() -> None:
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
            "temperature_2m_mean",
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
        check_dependencies()
    except ImportError as e:
        exit(str(e))

    print()
    print("Requesting data...")
    try:
        data = request_data()
    except IOError as e:
        exit(str(e))

    print("Analyzing Matrix data...")
    from pandas import DataFrame, to_datetime

    data_frame = DataFrame(data)
    data_frame = data_frame.dropna()
    data_frame["time"] = to_datetime(data_frame["time"])

    print(f"Processing {data_frame.shape[0]} data points...")

    time = data_frame["time"]
    temp_min = data_frame["apparent_temperature_min"]
    temp_max = data_frame["apparent_temperature_max"]
    temp = data_frame["temperature_2m_mean"]

    print("Generating visualization...")
    from matplotlib import pyplot as plot

    figure, axes = plot.subplots(figsize=(12, 8), dpi=120)

    figure.autofmt_xdate()
    axes.fill_between(
        x=time,
        y1=temp_min,
        y2=temp_max,
        alpha=0.3,
        color="orange",
        label="apparent temperature range",
    )
    axes.plot(
        time,
        temp,
        color="red",
        linewidth=3,
        marker="o",
        markersize=5,
        label="average temperature",
    )
    axes.set_title(
        "Zion (42 Kocaeli) Temperature Over Time\nwith Apparent Range",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )
    axes.set_xlim(time.min(), time.max())
    axes.set_xlabel("Date")
    axes.set_ylabel("Temperature (°C)")
    axes.legend()
    axes.grid()
    axes.spines["top"].set_visible(False)
    axes.spines["bottom"].set_visible(False)

    save_file = "matrix_analysis.png"
    plot.savefig(save_file)
    plot.show()

    print()
    print("Analysis complete!")
    print("Results saved to:", save_file)


if __name__ == "__main__":
    main()
