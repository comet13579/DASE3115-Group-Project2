import csv
from collections import defaultdict
from typing import Dict, List, Optional


class RiskFree:
    """Load a CSV with Year, Month, and a single value column.

    Stores data as: dict[int, List[Optional[float]]]
    - key: year (int)
    - value: list of length 13 where index 1..12 correspond to months

    Usage:
        rf = RiskFree('riskfree.csv')
        value = rf.get(1926, 7)
        # or access year map: rf[1926][7]
    """

    def __init__(self, path: str):
        self.path = path
        self._name: Optional[str] = None
        self.data: Dict[int, List[Optional[float]]] = defaultdict(dict)
        self._load()

    def _load(self) -> None:
        with open(self.path, newline='') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError('CSV is empty')

            if len(header) < 3:
                raise ValueError('CSV must have at least year, month, and one value column')

            # single value column name
            self._name = header[2].strip()

            for row in reader:
                if not row:
                    continue
                if len(row) < 3:
                    continue
                year_raw = row[0].strip()
                month_raw = row[1].strip()
                try:
                    year = int(year_raw)
                    month = int(month_raw)
                except ValueError:
                    continue

                val_raw = row[2].strip()
                if val_raw == '':
                    val = None
                else:
                    try:
                        val = float(val_raw)
                    except ValueError:
                        val = None

                # Initialize year list if needed
                if year not in self.data:
                    self.data[year] = [None] * 13
                self.data[year][month] = val

    def get(self, year: int, month: int) -> Optional[float]:
        """Return the value for year/month or None if missing."""
        try:
            return self.data[year][month]
        except Exception:
            return None

    def __getitem__(self, year: int) -> List[Optional[float]]:
        """Return the month list for a year (index 1..12)."""
        return self.data[year]

    def as_dict(self) -> Dict[int, List[Optional[float]]]:
        """Return the raw mapping year -> month-list."""
        return dict(self.data)

    @property
    def name(self) -> Optional[str]:
        return self._name


if __name__ == '__main__':
    # quick demo when run directly (expects `riskfree.csv` next to this file)
    import os
    path = os.path.join(os.path.dirname(__file__), 'risk-free.csv')
    rf = RiskFree(path)
    print('Column name:', rf.name)
    # print first few year-months found
    for y in sorted(rf.as_dict().keys())[:5]:
        print(y, rf[y][1:13])

