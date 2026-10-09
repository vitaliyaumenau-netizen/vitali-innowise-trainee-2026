import pandas as pd

class ReadData:

    def __init__(self, filename):
        self._df = pd.read_json(f"data/{filename}")
        self._df = self._df.where(pd.notnull(self._df), None)

    def read_data(self):
        if "birthday" in self._df.columns:
            self._df["birthday"] = pd.to_datetime(self._df["birthday"])
        return self._df

    def get_columns(self):
        return self._df.columns

    def print_data(self):
        print(self._df)

