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

1. Filter Graph - plainly graphs the filters you chose over the time period you choose
2. Filter Pie Chart - gives a pie chart based on the same filter you choose to show overall rates (success, fail, as a super or subset of your filter selections)
3. Success rate over time - looks at the company given the time frame to tell you their success rate over time.

Each of these provides a particular insight I find interesting and helpful for a consumer of my dashboard.

**Filter Graph** - I find this to be the default visualization of what you select in your filters. It is also interesting to see the range of missions vary over the given time frame of all or a subset of companies. It also gives you the ability to see statuses change over time. I.E; How NASA stopped launching in 2012 but haven't had a failure since 2004 despite have 23 launches between that time period all be successful.

**Filter Pie Chart** - While this pie chart isn't as effective when you're searching only 1 status, seeing the split of a certain subset or superset of statuses can also provide interesting insights. For instance, did you know that 35% of all NASA failures were partial failures leaving 65% of fails to be total failures, while not having any prelaunch failures? I'd be able to come up with some sort of an analysis with better research and knowledge of those particular instances versus a company that has a different distribution of failures.

**Success Rate Over Time** - I find this to be the most insightful data point given my limited experience. If I was in a position to have some reason (business or personal) to launch a space mission, I'd be able to see directly how a company's success rate varies over the past 20 years. Does it increase? Does it decrease? What does that mean in terms of how reliable they are in making rockets? In an anecdotal example, I'd be more likely to contract CASC than SpaceX with the knowledge that CASC has a proven track record of 100% success rate, with a high launch count in the past 20 years, where SpaceX only has less years of 100% success rate, and appear to be less consistent as a whole (not accounting for their innovations)

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
