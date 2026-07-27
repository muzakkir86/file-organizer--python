import pandas as pd
from pathlib import Path


def generate_documented_excel(csv_path: str, excel_path: str):
	df = pd.read_csv(csv_path)

	# Build documentation DataFrame
	docs = []
	for col in df.columns:
		col_series = df[col]
		docs.append({
			'column': col,
			'dtype': str(col_series.dtype),
			'non_null_count': int(col_series.count()),
			'unique_values': int(col_series.nunique(dropna=True)),
			'sample_value': col_series.dropna().astype(str).head(3).tolist(),
		})

	doc_df = pd.DataFrame(docs)

	# Summary statistics for numeric columns
	numeric_summary = df.select_dtypes(include='number').describe().T

	# Write to Excel with multiple sheets
	with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
		df.to_excel(writer, sheet_name='Data', index=False)
		doc_df.to_excel(writer, sheet_name='Documentation', index=False)
		numeric_summary.to_excel(writer, sheet_name='Numeric_Summary')


def main():
	base = Path(__file__).parent
	csv_path = base / 'sales_summary.csv'
	excel_path = base / 'production_report.xlsx'

	generate_documented_excel(str(csv_path), str(excel_path))
	print(f'Wrote Excel file: {excel_path.name}')


if __name__ == '__main__':
	main()

