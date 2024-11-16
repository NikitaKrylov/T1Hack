from io import BytesIO

import pandas as pd


def file_to_pandas_dataframe(file_content: bytes, skip_rows: int = 0):
    io = BytesIO(file_content)
    return pd.read_csv(io, skip_blank_lines=True, skiprows=skip_rows, sep=';')
