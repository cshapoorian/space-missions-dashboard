# Space Missions Dashboard

An interactive data visualization dashboard for exploring historical space mission records from 1957 to present. Built with Python, Streamlit, and Plotly.

## Features

- **Interactive Filters**: Filter missions by year range, company, and mission status
- **Real-time Metrics**: View total missions, success rate, unique companies, and rockets at a glance
- **Dynamic Visualizations**:
  - Timeline chart showing missions per year
  - Pie chart displaying mission status distribution
- **Sortable Data Table**: Browse and sort through all mission records
- **Data Analysis API**: 8 purpose-built functions for querying mission data

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd space-missions-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   cd src
   streamlit run dashboard.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## Usage

### Running the Dashboard

Once launched, the dashboard will be available at **http://localhost:8501**. Use the sidebar controls to:

- **Year Range**: Drag the slider to filter missions within a specific time period
- **Companies**: Select one or more space agencies/companies to focus on
- **Status**: Filter by mission outcome (Success, Failure, Partial Failure, Prelaunch Failure)

### Data Analysis Functions

The `data_functions.py` module provides 8 functions for programmatic data analysis:

| Function | Description | Returns |
|----------|-------------|---------|
| `getMissionCountByCompany(companyName)` | Count of missions by a specific company | `int` |
| `getSuccessRate(companyName)` | Success rate percentage for a company | `float` (2 decimals) |
| `getMissionsByDateRange(startDate, endDate)` | List of mission names within date range | `list[str]` |
| `getTopCompaniesByMissionCount(n)` | Top N companies by mission count | `list[tuple]` |
| `getMissionStatusCount()` | Count of missions by status | `dict` |
| `getMissionsByYear(year)` | Number of missions in a given year | `int` |
| `getMostUsedRocket()` | Name of the most frequently used rocket | `str` |
| `getAverageMissionsPerYear(startYear, endYear)` | Average missions per year in range | `float` (2 decimals) |

**Example usage:**
```python
from data_functions import getSuccessRate, getTopCompaniesByMissionCount

# Get NASA's success rate
rate = getSuccessRate("NASA")  # Returns: 91.63

# Get top 3 companies by mission count
top = getTopCompaniesByMissionCount(3)
# Returns: [('RVSN USSR', 1777), ('CASC', 338), ('Arianespace', 293)]
```

## Running Tests

```bash
# From project root
pytest tests/ -v
```

All 24 tests should pass, covering edge cases for each data function.

## Project Structure

```
space-missions-dashboard/
├── data/
│   └── space_missions.csv    # Dataset (4,630 missions)
├── src/
│   ├── __init__.py
│   ├── dashboard.py          # Streamlit dashboard application
│   └── data_functions.py     # Data analysis functions
├── tests/
│   ├── __init__.py
│   └── test_functions.py     # Unit tests
├── pyproject.toml            # Project configuration
├── requirements.txt          # Python dependencies
└── README.md
```

## Dataset

The dashboard uses a comprehensive dataset of **4,630 space missions** spanning from 1957 to 2022, including:

| Column | Description |
|--------|-------------|
| Company | Organization responsible for the mission |
| Location | Launch site location |
| Date | Launch date |
| Time | Launch time (UTC) |
| Rocket | Rocket/launch vehicle name |
| Mission | Mission name |
| RocketStatus | Current status of the rocket type |
| Price | Mission cost (where available) |
| MissionStatus | Outcome (Success, Failure, Partial Failure, Prelaunch Failure) |

## Technology Stack

- **Python 3.9+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pytest**: Testing framework
