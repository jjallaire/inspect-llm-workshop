# import queries.csv dataset for use with evals from full results.csv dataset

import re
import pandas as pd

# pull out the 'COLUMNS' from the full_prompt field
def extract_columns(full_prompt):
    match = re.search(r"COLUMNS:([^\"\n]+)", full_prompt)
    return match.group(1) if match else ''

# read the csv
df = pd.read_csv("results.csv")

# extract + rename the user_input and columns 
df['columns'] = df['JOIN::::app.nlq.full_prompt'].apply(extract_columns)
result_df = df[['app.nlq.user_input', 'columns']].rename(columns={'app.nlq.user_input': 'user_input'})

# write to eval dataset csv
result_df.to_csv("queries.csv", index=False)
