import pandas as pd

def parse_answer_key(file_path):
    """Parse the answer key Excel file and return a DataFrame."""
    return pd.read_excel(file_path)
