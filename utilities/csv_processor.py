import polars as pl

def read_asset_data(file_path):
    return pl.read_csv(file_path)

def write_output_data(file_path, output_data):
    output_data.write_csv(file_path)
