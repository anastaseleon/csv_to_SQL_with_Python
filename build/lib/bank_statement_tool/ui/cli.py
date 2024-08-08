import click
import pandas as pd
import os
import pkg_resources
from bank_statement_tool.importer import load_bank_statement, append_transactions
from bank_statement_tool.categorizer import categorize_transactions, calculate_total

@click.group()
def cli():
    pass

@click.command()
@click.argument('filename')
@click.option('--encoding', default='utf-8', help='File encoding (default is utf-8)')
def import_statement(filename, encoding):
    df = load_bank_statement(filename, encoding=encoding)
    print("DataFrame Loaded:")
    print(df.head())  # Print the first few rows to confirm data
    append_transactions('transactions.csv', df)
    click.echo(f"Imported transactions from {filename} with encoding {encoding}")

@click.command()
def categorize():
    data_path = os.path.join(pkg_resources.resource_filename('bank_statement_tool', 'data'), 'transactions.csv')
    df = pd.read_csv(data_path)
    print("DataFrame Loaded for Categorization:")
    print(df.head())  # Print the first few rows to confirm data
    df = categorize_transactions(df)
    df.to_csv(data_path, index=False)
    click.echo("Transactions categorized and saved.")

@click.command()
def total():
    data_path = os.path.join(pkg_resources.resource_filename('bank_statement_tool', 'data'), 'transactions.csv')
    df = pd.read_csv(data_path)
    totals = calculate_total(df)
    click.echo("Total by category:")
    click.echo(totals)

cli.add_command(import_statement)
cli.add_command(categorize)
cli.add_command(total)

if __name__ == "__main__":
    cli()
