"""Data analysis functions for querying space mission records."""

import pandas as pd
from pathlib import Path

_df = None


def _load_data():
    """Load and cache CSV data."""
    global _df
    if _df is not None:
        return _df

    for p in [Path(__file__).parent.parent / "data" / "space_missions.csv", Path("space_missions.csv")]:
        if p.exists():
            _df = pd.read_csv(p)
            _df['Date'] = pd.to_datetime(_df['Date'], errors='coerce')
            return _df

    raise FileNotFoundError("space_missions.csv not found")


def getMissionCountByCompany(companyName: str) -> int:
    # Create boolean Series where Company matches, then sum True values (count matches)
    return int((_load_data()['Company'] == companyName).sum())


def getSuccessRate(companyName: str) -> float:
    df = _load_data()
    # Filter DataFrame to only rows where Company column equals companyName
    co = df[df['Company'] == companyName]
    if co.empty:
        return 0.0
    # Count successful missions, divide by total, multiply by 100 for percentage
    return round((co['MissionStatus'] == 'Success').sum() / len(co) * 100, 2)


def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    df = _load_data()
    try:
        start, end = pd.to_datetime(startDate), pd.to_datetime(endDate)
    except:
        return []
    if start > end:
        return []
    # Create boolean mask: True for rows where Date falls within range (inclusive)
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    # Apply mask to filter rows, sort by date, extract Mission column as list
    return df[mask].sort_values('Date')['Mission'].tolist()


def getTopCompaniesByMissionCount(n: int) -> list:
    if n <= 0:
        return []
    df = _load_data()
    # Group by Company, count rows per group, convert to DataFrame with 'c' column
    counts = df.groupby('Company').size().reset_index(name='c')
    # Sort by count descending, then alphabetically for ties
    counts = counts.sort_values(['c', 'Company'], ascending=[False, True])
    # Take top n rows, convert each row to (company_name, count) tuple
    return [(r['Company'], int(r['c'])) for _, r in counts.head(n).iterrows()]


def getMissionStatusCount() -> dict:
    # Get counts of each unique MissionStatus value as dictionary
    counts = _load_data()['MissionStatus'].value_counts().to_dict()
    # Return dict with fixed key order, defaulting to 0 if status not present
    return {k: int(counts.get(k, 0)) for k in ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]}


def getMissionsByYear(year: int) -> int:
    # Extract year from Date column, compare to target year, sum matching rows
    return int((_load_data()['Date'].dt.year == year).sum())


def getMostUsedRocket() -> str:
    df = _load_data()
    # Group by Rocket, count missions per rocket
    counts = df.groupby('Rocket').size().reset_index(name='c')
    # Filter to only rockets with max count, sort alphabetically for consistent tie-breaking
    top = counts[counts['c'] == counts['c'].max()].sort_values('Rocket')
    return top.iloc[0]['Rocket']


def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    if startYear > endYear:
        return 0.0
    df = _load_data()
    # Boolean mask: True for each mission within the year range
    mask = (df['Date'].dt.year >= startYear) & (df['Date'].dt.year <= endYear)
    # Sum matching missions, divide by number of years in range (inclusive)
    return round(mask.sum() / (endYear - startYear + 1), 2)
