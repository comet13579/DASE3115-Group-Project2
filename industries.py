import csv
from collections import defaultdict
from typing import Dict, List, Optional


class Industries:
    """Load the CSV and provide access as industries[type][year][month].

    Structure: dict[str, dict[int, List[Optional[float]]]]
    - Outer dict key: industry name (string)
    - Inner dict key: year (int)
    - Inner dict value: list of length 13 where index 1..12 are months

    Usage:
        data = Industries('industries.csv')
        value = data['Food'][1926][7]
    """

    def __init__(self, path: str):
        self.path = path
        # type: Dict[str, Dict[int, List[Optional[float]]]]
        self.industries: Dict[str, Dict[int, List[Optional[float]]]] = defaultdict(dict)
        self._load()

    def _load(self) -> None:
        with open(self.path, newline='') as f:
            reader = csv.reader(f)
            # Read header
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError('CSV is empty')

            # Header has first two columns for year,month (often empty labels)
            # Remaining columns are industry types; strip whitespace
            if len(header) < 3:
                raise ValueError('CSV header must contain at least year,month and one industry')

            industry_names = [h.strip() for h in header[2:]]

            # Initialize dictionaries for each industry
            for name in industry_names:
                # inner dict will map year -> list[0..12], index 1..12 used
                self.industries[name] = {}

            for row in reader:
                if not row:
                    continue
                # some rows may contain extra spaces - strip
                # Expect at least year, month + as many industry columns
                if len(row) < 3:
                    continue
                year_raw = row[0].strip()
                month_raw = row[1].strip()
                try:
                    year = int(year_raw)
                    month = int(month_raw)
                except ValueError:
                    # skip malformed rows
                    continue

                # Parse industry values; there may be fewer values than header
                values = []
                for v in row[2:2 + len(industry_names)]:
                    sv = v.strip()
                    if sv == '':
                        values.append(None)
                    else:
                        try:
                            values.append(float(sv))
                        except ValueError:
                            values.append(None)

                # pad missing values
                while len(values) < len(industry_names):
                    values.append(None)

                # Store each value into the corresponding industry's year->month list
                for name, val in zip(industry_names, values):
                    year_map = self.industries.setdefault(name, {})
                    if year not in year_map:
                        # create list index 0..12; index 0 unused to allow 1-based months
                        year_map[year] = [None] * 13
                    year_map[year][month] = val

    def get(self, industry: str, year: int, month: int) -> Optional[float]:
        """Return the value or None if not present."""
        try:
            return self.industries[industry][year][month]
        except Exception:
            return None

    def industries_list(self) -> List[str]:
        """Return the list of industry names."""
        return list(self.industries.keys())

    def __getitem__(self, industry: str):
        """Allow bracket access: instance[industry] returns dict year->list."""
        return self.industries[industry]

    def as_dict(self) -> Dict[str, Dict[int, List[Optional[float]]]]:
        """Return the raw nested dict structure."""
        return self.industries


if __name__ == '__main__':
    csv_path = 'industries.csv'
    data = Industries(csv_path)

	# Example access: industries[type][year][month]
	# Using the Industries instance directly supports bracket access:
	#   data['Food'][1926][7]
    samples = [
		('Beer', 2019, 3),
		('Beer', 1926, 8),
		('Smoke', 1927, 12),
		('Meals', 2010, 12),
	]
    print(data.industries_list())
    for i in range(2019,2009,-1):
        val = data.get("Beer",i,3)
        print(f"BEER {i}-{3}: {val}")