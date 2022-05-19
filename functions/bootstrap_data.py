import sys

sys.path.append(".")

import databutton as db
import pandas as pd
from lib.config import DATA_KEY


# Used to clear the remote dataframe if needed
def main():
    df = pd.read_csv("./data/structure.csv")
    db.dataframes.put(df, DATA_KEY)


if __name__ == "__main__":
    main()
