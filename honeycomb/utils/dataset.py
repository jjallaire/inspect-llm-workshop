

from inspect_ai.dataset import csv_dataset, FieldSpec

def read_user_queries():
    dataset = csv_dataset(
        csv_file="data/queries.csv",
        sample_fields=FieldSpec(
            input="user_input",
            metadata=["columns"]
        ),
        shuffle=True
    )
    return dataset

