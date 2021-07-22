from pandas.api.types import CategoricalDtype

import pandas as pd
import os

working_dir: str = "working"
input_csv: str = os.path.join(working_dir, "debug_export.csv")
output_csv: str = os.path.join(working_dir, "debug_last_instance.csv")

suit_categories = ["Spade", "Heart", "Club", "Diamond", "Black", "Red"]
value_categories = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Joker"]
codes_categories = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC', 'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD', 'OB', 'OR']

dtypes: dict = {
    "suit": CategoricalDtype(categories=suit_categories, ordered=True),
    "value": CategoricalDtype(categories=value_categories, ordered=True),
    "code": CategoricalDtype(categories=codes_categories, ordered=True),
    "remaining": "uint64",
    "starting": "uint64",
    "times_seen": "uint64"
}

if __name__ == "__main__":
    df = pd.read_csv(input_csv, dtype=dtypes)

    print("Pre-Drop Most Cards")
    print("-"*10)
    df.info(verbose=False, memory_usage="deep")

    df = df[df["times_seen"] == 6000000]

    print("Post-Drop Most Cards")
    print("-"*10)
    df.info(verbose=False, memory_usage="deep")

    print("Resulting DataFrame")
    print("-"*10)
    print(df)

    print("Exporting Non-Dropped Cards")
    df.to_csv(output_csv, index=True)

    print("Done!!!")
