"""Interactive Streamlit dashboard for exploring historical space mission data."""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

CHART_CONFIG = {'displayModeBar': False}


@st.cache_data
def load_data():
    for path in [Path(__file__).parent.parent / "data" / "space_missions.csv", Path("space_missions.csv")]:
        if path.exists():
            df = pd.read_csv(path)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            return df
    raise FileNotFoundError("space_missions.csv not found")


def main():
    st.set_page_config(page_title="Space Missions", layout="wide")
    st.title("Space Missions Dashboard")

    df = load_data()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        min_yr, max_yr = int(df['Year'].min()), int(df['Year'].max())
        year_range = st.slider("Year Range", min_yr, max_yr, (min_yr, max_yr))
        companies = st.multiselect("Companies", sorted(df['Company'].unique()))
        statuses = st.multiselect("Status", df['MissionStatus'].unique())

    # Apply filters
    data = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if companies:
        data = data[data['Company'].isin(companies)]
    if statuses:
        data = data[data['MissionStatus'].isin(statuses)]

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Missions", f"{len(data):,}")
    rate = (data['MissionStatus'] == 'Success').mean() * 100 if len(data) else 0
    c2.metric("Success Rate", f"{rate:.1f}%")
    c3.metric("Companies", data['Company'].nunique())
    c4.metric("Rockets", data['Rocket'].nunique())

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        # Fill in years with 0 missions so chart shows gaps
        all_years = pd.DataFrame({'Year': range(year_range[0], year_range[1] + 1)})
        by_year = data.groupby('Year').size().reset_index(name='count')
        by_year = all_years.merge(by_year, on='Year', how='left').fillna(0).astype({'count': int})
        fig = px.line(by_year, x='Year', y='count', markers=True)
        fig.update_layout(yaxis_title="Missions", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

    with col2:
        counts = data['MissionStatus'].value_counts()
        fig = px.pie(counts, values=counts.values, names=counts.index)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

    # Data table
    st.subheader(f"Data ({len(data):,} missions)")
    display = data[['Mission', 'Company', 'Date', 'Rocket', 'Location', 'MissionStatus']].copy()
    display['Date'] = display['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(display.sort_values('Date', ascending=False), height=400, hide_index=True)


if __name__ == "__main__":
    main()
