from pathlib import Path
import pandas as pd

class csvLoader:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        data = pd.read_csv(
            self.file_path,
            header = [0, 1]
        )

        symbol = data.columns[1][1]

        data.columns = [
            "timestamp",
            "close",
            "high",
            "low",
            "open",
            "volume"
        ]

        data["symbol"] = symbol
        data["timestamp"] = pd.to_datetime(data["timestamp"], format="%Y-%m-%d", errors = "coerce")
        data = data.dropna(subset = ["timestamp"])

        data = data[
            [
                "timestamp",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        ]

        data.sort_values("timestamp", inplace = True)
        data.reset_index(drop = True, inplace = True)

        return data