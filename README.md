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

### Approach

I use 3 different visualizations in this project:

**1. Success Rate Over Time** Looks at the companies given the time frame to tell you their success rate over time (can be compare to the alltime total, and against other companies). I chose this because the success rate is what people look at when they think of reliability, which in my limited knowledge, is the most important factor when considering a aerospace company.

**2. Selected Missions** This allows you to compare companies given the selected status, whether it is successes, failures, different failure types, etc. I chose this because this gives you full access to compare and contrast using the full range of filters of the available data. It customizability is guaranteed to give any user the data they are looking for.

**3. Successes vs Failures by Year** This allows for the user to see the whole number of success vs fails when combining companies, looking at just 1, or looking at all companies. This aggregates the data of companies that are filtered together for visual clarity purposes. I chose this because it directly shows the number of mission successes, and total number of fails in a directly comparable way. This allows the user to either track trends over the years, look at a set of companies' performance, or other similar metric that the user values.

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

### Running the Dashboard

Once launched, the dashboard will be available at **http://localhost:8501**.

## Technology Stack

- **Python 3.9+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pytest**: Testing framework
