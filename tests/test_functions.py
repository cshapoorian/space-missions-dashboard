"""Unit tests for data analysis functions."""

import pytest
from data_functions import (
    getMissionCountByCompany,
    getSuccessRate,
    getMissionsByDateRange,
    getTopCompaniesByMissionCount,
    getMissionStatusCount,
    getMissionsByYear,
    getMostUsedRocket,
    getAverageMissionsPerYear,
)


# getMissionCountByCompany

def test_count_valid():
    assert getMissionCountByCompany("NASA") > 0

def test_count_invalid():
    assert getMissionCountByCompany("FakeCompany") == 0

def test_count_empty():
    assert getMissionCountByCompany("") == 0

def test_count_case_sensitive():
    assert getMissionCountByCompany("NASA") == 203
    assert getMissionCountByCompany("nasa") == 0


# getSuccessRate

def test_rate_valid():
    assert getSuccessRate("NASA") == 91.63

def test_rate_invalid():
    assert getSuccessRate("FakeCompany") == 0.0

def test_rate_decimals():
    r = getSuccessRate("SpaceX")
    assert len(str(r).split('.')[-1]) <= 2


# getMissionsByDateRange

def test_range_valid():
    m = getMissionsByDateRange("1957-10-01", "1957-12-31")
    assert m == ["Sputnik-1", "Sputnik-2", "Vanguard TV3"]

def test_range_empty():
    assert getMissionsByDateRange("1900-01-01", "1900-12-31") == []

def test_range_reversed():
    assert getMissionsByDateRange("2020-12-31", "2020-01-01") == []

def test_range_invalid():
    assert getMissionsByDateRange("bad", "date") == []


# getTopCompaniesByMissionCount
def test_top_valid():
    assert getTopCompaniesByMissionCount(3) == [("RVSN USSR", 1777), ("CASC", 338), ("Arianespace", 293)]

def test_top_zero():
    assert getTopCompaniesByMissionCount(0) == []

def test_top_negative():
    assert getTopCompaniesByMissionCount(-1) == []


# getMissionStatusCount

def test_status_keys():
    assert getMissionStatusCount() == {"Success": 4162, "Failure": 357, "Partial Failure": 107, "Prelaunch Failure": 4}

def test_status_types():
    c = getMissionStatusCount()
    assert all(isinstance(v, int) for v in c.values())


# getMissionsByYear
def test_year_valid():
    assert getMissionsByYear(2020) == 119

def test_year_none():
    assert getMissionsByYear(1900) == 0


# getMostUsedRocket
def test_rocket_valid():
    assert getMostUsedRocket() == "Cosmos-3M (11K65M)"

def test_rocket_consistent():
    assert getMostUsedRocket() == getMostUsedRocket()


# getAverageMissionsPerYear
def test_avg_valid():
    assert getAverageMissionsPerYear(2010, 2020) == 72.27

def test_avg_single():
    assert getAverageMissionsPerYear(2020, 2020) == getMissionsByYear(2020)

def test_avg_reversed():
    assert getAverageMissionsPerYear(2020, 2010) == 0.0

def test_avg_decimals():
    a = getAverageMissionsPerYear(2000, 2020)
    assert len(str(a).split('.')[-1]) <= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
