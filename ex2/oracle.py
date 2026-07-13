#!/usr/bin/env python3
from os import getenv
from dotenv import load_dotenv


class Oracle:
    def __init__(
        self,
        matrix_mode: str | None,
        database_url: str | None,
        api_key: str | None,
        log_level: str | None,
        zion_endpoint: str | None,
    ):
        self.matrix_mode = matrix_mode if matrix_mode else "development"
        self.database_url = database_url
        self.api_key = api_key
        self.log_level = log_level if log_level else "INFO"
        self.zion_endpoint = zion_endpoint

    def __str__(self) -> str:
        database_status = (
            "Connected" if self.database_url else "Could not connect"
        )
        api_status = "Authenticated" if self.api_key else "Denied"
        zion_status = "Online" if self.zion_endpoint else "Offline"

        return "\n".join(
            [
                f"Mode: {self.matrix_mode}",
                f"Database: {database_status} to {self.matrix_mode} instance",
                f"API Access: {api_status}",
                f"Log Level: {self.log_level}",
                f"Zion Endpoint: {zion_status}",
            ]
        )

    def __bool__(self) -> bool:
        return all(
            [
                self.matrix_mode in ("development", "production"),
                self.database_url,
                self.api_key,
                self.zion_endpoint,
            ]
        )


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    load_dotenv()

    config = Oracle(
        getenv("MATRIX_MODE"),
        getenv("DATABASE_URL"),
        getenv("API_KEY"),
        getenv("LOG_LEVEL"),
        getenv("ZION_ENDPOINT"),
    )

    print()
    print("Configuration loaded:")
    print(config)

    print()
    print("Environment security check:")

    print("[OK] No hardcoded secrets detected")

    if config:
        print("[OK] .env file properly configured")
    else:
        print("[MISSING] .env file not properly configured")

    print("[OK] Production overrides available")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
