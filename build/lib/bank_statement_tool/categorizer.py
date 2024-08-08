import pandas as pd

def categorize_transactions(df):
    df['Category'] = None
    for index, row in df.iterrows():
        print(f"Transaction: {row['Description']} - {row['Amount']}")
        category = input("Enter category: ")
        df.at[index, 'Category'] = category
    return df

def calculate_total(df):
    return df.groupby('Category')['Amount'].sum()

