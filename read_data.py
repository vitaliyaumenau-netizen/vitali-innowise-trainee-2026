import pandas as pd

class ReadData:

    def __init__(self, filename):
        self._df = pd.read_json(f"data/{filename}")
        self._df = self._df.where(pd.notnull(self._df), None)

        if "room" in self._df.columns:
            self._separated_data = self._df[["id", "room"]].copy()
            if self._separated_data is not None:
                self._separated_data.rename(columns={"id": "student"}, inplace=True)
        else:
            self._separated_data = None

    def read_data(self):
        if "birthday" in self._df.columns:
            self._df["birthday"] = pd.to_datetime(self._df["birthday"])
        return self._df

    def extract_student_with_room(self):
       return self._separated_data

    def get_columns(self):
        return [col for col in self._df.columns if col != 'room']

    def print_data(self):
        print(self._df)

