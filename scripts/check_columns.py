import pandas as pd

# Load your data
df = pd.read_csv('../dataset/train.csv')

# Print the list of all column names
print("Columns in dataset:")
print(df.columns.tolist())