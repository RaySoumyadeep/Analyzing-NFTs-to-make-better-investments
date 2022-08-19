# Importing Pandas for Data wrangling and cleaning
import pandas as pd

# Reading the scraped data from CSV
data = pd.read_csv('data/scraped.csv', index_col=[0])

# Dropping the rows wherever CAT_Number is NULL
data = data.dropna(subset=['cat_number'])

# Splitting the String Data inot appropriate columns
data[['cat_number', 'rank']] = data['cat_number'].str.split('\n', expand=True)
data[['face', 'face-score']] = data['face'].str.split('+', expand=True)
data[['shirt', 'shirt-score']] = data['shirt'].str.split('+', expand=True)
data[['tier', 'tier-score']] = data['tier'].str.split('+', expand=True)
data[['hats', 'hats-score']] = data['hats'].str.split('+', expand=True)

# Filling the null values with appropriate scalers according to business problem
data['face-score'].fillna(0, inplace=True)
data['face-score'].isna().sum()

data['shirt-score'].fillna(0, inplace=True)
data['shirt-score'].isna().sum()

data['tier-score'].fillna(4, inplace=True)
data['tier-score'].isna().sum()

data['hats-score'].fillna(5, inplace=True)
data['hats-score'].isna().sum()

# Dropping redundent column
data.drop(columns='Total', index=1, inplace=True)

# Removing extra text from the Columns
data['cat_number'] = data['cat_number'].str[10:]
data['rank'] = data['rank'].str[6:]

# Stripping the data from Characteristic columns
data['face'] = data['face'].str.strip()
data['shirt'] = data['shirt'].str.strip()
data['tier'] = data['tier'].str.strip()
data['hats'] = data['hats'].str.strip()

# Verifying all the null values are handled
data.isna().sum()

# Exporting the dataset to Data directory in CSV format
data.to_csv('data/final_dataset.csv', header=True)