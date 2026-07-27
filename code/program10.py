"""Advanced Python + pandas example.

This script generates sample sales data and analyzes it with pandas.
It uses dataclasses, type hints, generators, context managers, and clean code.
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Generator, List

import pandas as pd


@dataclass
class SaleRecord:
    date: datetime
    region: str
    product: str
    units: int
    price: float

    @property
    def revenue(self) -> float:
        return self.units * self.price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "region": self.region,
            "product": self.product,
            "units": self.units,
            "price": self.price,
            "revenue": round(self.revenue, 2),
        }


def generate_sales(
    start_date: datetime,
    days: int,
    regions: List[str],
    products: List[str],
) -> Generator[SaleRecord, None, None]:
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        for region in regions:
            for product in products:
                yield SaleRecord(
                    date=current_date,
                    region=region,
                    product=product,
                    units=random.randint(5, 30),
                    price=round(random.uniform(10.0, 80.0), 2),
                )


@contextmanager
def timer(task_name: str):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{task_name} took {elapsed:.2f} seconds")


def build_dataframe(records: Generator[SaleRecord, None, None]) -> pd.DataFrame:
    with timer("Build DataFrame"):
        rows = [record.to_dict() for record in records]
        return pd.DataFrame(rows)


def analyze_sales(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = df["units"] * df["price"]

    summary = (
        df.groupby(["region", "product"], as_index=False)
        .agg(total_units=("units", "sum"), total_revenue=("revenue", "sum"))
        .sort_values(["region", "total_revenue"], ascending=[True, False])
    )
    return summary


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved summary to: {path}")


def main(days: int = 7, output_file: str = "sales_summary.csv") -> None:
    print("Advanced Python + pandas demo")
    print("Generating sample sales data...")

    start_date = datetime.today() - timedelta(days=days)
    records = generate_sales(
        start_date=start_date,
        days=days,
        regions=["North", "South", "East", "West"],
        products=["Widget", "Gadget", "Doohickey"],
    )

    df = build_dataframe(records)
    print("\nSample data:")
    print(df.head(6).to_string(index=False))

    summary = analyze_sales(df)
    print("\nSales summary by region and product:")
    print(summary.to_string(index=False))

    save_csv(summary, Path(output_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an advanced Python + pandas sales analysis example."
    )
    parser.add_argument("--days", type=int, default=7, help="Number of days of data to generate")
    parser.add_argument("--output", default="sales_summary.csv", help="Output CSV file name")
    args = parser.parse_args()

    try:
        main(days=args.days, output_file=args.output)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
