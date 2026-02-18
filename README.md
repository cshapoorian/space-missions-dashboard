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
   git clone https://github.com/cshapoorian/space-missions-dashboard.git
   cd space-missions-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:

   **Windows (Command Prompt or PowerShell):**
   ```cmd
   cd src
   python -m streamlit run dashboard.py
   ```

   **Linux / macOS (Terminal):**
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

Once launched, the dashboard will be available at **http://localhost:8501**.

## Technology Stack

- **Python 3.9+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pytest**: Testing framework
