import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

CHART_CONFIG = {'displayModeBar': False}


@st.cache_data
def load_data():
    for path in [Path(__file__).parent / "space_missions.csv", Path("space_missions.csv")]:
        if path.exists():
            df = pd.read_csv(path)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            return df
    raise FileNotFoundError("space_missions.csv not found")


def main():
    st.set_page_config(page_title="Space Missions", layout="wide")

    # Hide deploy button, hamburger menu, footer, and reduce top padding
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display: none;}
            .block-container {padding-top: 1rem;}
            section[data-testid="stSidebar"] > div:first-child {padding-top: 1rem;}
        </style>
    """, unsafe_allow_html=True)

    st.title("Space Missions Dashboard")

    df = load_data()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        min_yr, max_yr = int(df['Year'].min()), int(df['Year'].max())
        year_range = st.slider("Year Range", min_yr, max_yr, (min_yr, max_yr))
        company_options = ["All"] + sorted(df['Company'].unique())
        companies = st.multiselect("Companies", company_options, default=["All"])
        statuses = st.multiselect("Status", df['MissionStatus'].unique())

    # Apply filters
    # Base data filtered by year and company (for success rate chart - not affected by status)
    base_data = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    selected_companies = companies if companies else ["All"]
    specific_companies = [c for c in companies if c != "All"]
    if specific_companies and "All" not in companies:
        base_data = base_data[base_data['Company'].isin(specific_companies)]

    # Filtered data (includes status filter for missions chart, bar graph, and table)
    data = base_data.copy()
    if statuses:
        data = data[data['MissionStatus'].isin(statuses)]

    # Build descriptive labels based on filters
    status_desc = ""
    if statuses:
        if len(statuses) == 1:
            status_map = {"Success": "successful", "Failure": "failed", "Partial Failure": "partially failed", "Prelaunch Failure": "prelaunch failed"}
            status_desc = status_map.get(statuses[0], statuses[0].lower()) + " "
        else:
            status_desc = "selected "

    company_desc = ""
    if "All" in selected_companies or not specific_companies:
        company_desc = "across all companies"
    elif len(specific_companies) == 1:
        company_desc = f"by {specific_companies[0]}"
    elif len(specific_companies) == 2:
        company_desc = f"by {specific_companies[0]} & {specific_companies[1]}"
    else:
        company_desc = f"by {len(specific_companies)} companies"

    year_desc = f"({year_range[0]}-{year_range[1]})" if year_range[0] != year_range[1] else f"({year_range[0]})"

    # Metrics with descriptive context
    st.markdown(f"### {len(data):,} {status_desc}missions {company_desc} {year_desc}")
    c1, c2, c3 = st.columns(3)
    rate = (data['MissionStatus'] == 'Success').mean() * 100 if len(data) else 0
    c1.metric("Success Rate", f"{rate:.1f}%")
    c2.metric("Companies", data['Company'].nunique())
    c3.metric("Rockets", data['Rocket'].nunique())

    # Primary chart: Success Rate Over Time (not affected by status filter)
    all_years = pd.DataFrame({'Year': range(year_range[0], year_range[1] + 1)})
    if len(base_data) > 0:
        if selected_companies == ["All"]:
            yearly_stats = base_data.groupby('Year').agg(
                total=('MissionStatus', 'count'),
                successes=('MissionStatus', lambda x: (x == 'Success').sum())
            ).reset_index()
            yearly_stats['SuccessRate'] = yearly_stats.apply(
                lambda row: round(row['successes'] / row['total'] * 100, 1) if row['total'] > 0 else None,
                axis=1
            )
            yearly_stats = all_years.merge(yearly_stats, on='Year', how='left')
            fig = px.line(yearly_stats.dropna(subset=['SuccessRate']), x='Year', y='SuccessRate', markers=True)
        else:
            chart_data = []
            for selection in selected_companies:
                if selection == "All":
                    sel_stats = base_data.groupby('Year').agg(
                        total=('MissionStatus', 'count'),
                        successes=('MissionStatus', lambda x: (x == 'Success').sum())
                    ).reset_index()
                else:
                    sel_stats = base_data[base_data['Company'] == selection].groupby('Year').agg(
                        total=('MissionStatus', 'count'),
                        successes=('MissionStatus', lambda x: (x == 'Success').sum())
                    ).reset_index()
                sel_stats['SuccessRate'] = sel_stats.apply(
                    lambda row: round(row['successes'] / row['total'] * 100, 1) if row['total'] > 0 else None,
                    axis=1
                )
                merged = all_years.merge(sel_stats, on='Year', how='left')
                merged['Company'] = selection
                chart_data.append(merged)
            yearly_stats = pd.concat(chart_data, ignore_index=True)
            fig = px.line(yearly_stats.dropna(subset=['SuccessRate']), x='Year', y='SuccessRate', color='Company', markers=True)
        fig.update_layout(
            title="Success Rate Over Time",
            margin=dict(t=40, b=10, l=10, r=10),
            yaxis_title="Success Rate (%)",
            xaxis_title="Year",
            yaxis=dict(range=[0, 105])
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
    else:
        st.info("No missions found for the selected filters.")

    # Secondary charts row
    col1, col2 = st.columns(2)

    with col1:
        # Selected Missions chart (dynamically trimmed to actual data range)
        if len(data) > 0:
            data_min_yr, data_max_yr = int(data['Year'].min()), int(data['Year'].max())
            dynamic_years = pd.DataFrame({'Year': range(data_min_yr, data_max_yr + 1)})
            if selected_companies == ["All"]:
                by_year = data.groupby('Year').size().reset_index(name='Missions')
                by_year = dynamic_years.merge(by_year, on='Year', how='left').fillna(0).astype({'Missions': int})
                fig = px.line(by_year, x='Year', y='Missions', markers=True)
            else:
                chart_data = []
                for selection in selected_companies:
                    if selection == "All":
                        sel_data = data.groupby('Year').size().reset_index(name='Missions')
                    else:
                        sel_data = data[data['Company'] == selection].groupby('Year').size().reset_index(name='Missions')
                    merged = dynamic_years.merge(sel_data, on='Year', how='left')
                    merged['Company'] = selection
                    merged['Missions'] = merged['Missions'].fillna(0).astype(int)
                    chart_data.append(merged)
                by_year = pd.concat(chart_data, ignore_index=True)
                fig = px.line(by_year, x='Year', y='Missions', color='Company', markers=True)
            fig.update_layout(
                title="Selected Missions",
                yaxis_title="Missions",
                margin=dict(t=40, b=10, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
        else:
            st.info("No missions found for the selected filters.")

    with col2:
        # Bar graph: Successes vs Failures by year (dynamically trimmed to actual data range)
        if len(base_data) > 0:
            base_min_yr, base_max_yr = int(base_data['Year'].min()), int(base_data['Year'].max())
            dynamic_years_base = pd.DataFrame({'Year': range(base_min_yr, base_max_yr + 1)})
            yearly_outcomes = base_data.groupby('Year').agg(
                Successes=('MissionStatus', lambda x: (x == 'Success').sum()),
                Failures=('MissionStatus', lambda x: (x != 'Success').sum())
            ).reset_index()
            yearly_outcomes = dynamic_years_base.merge(yearly_outcomes, on='Year', how='left').fillna(0)
            yearly_outcomes['Successes'] = yearly_outcomes['Successes'].astype(int)
            yearly_outcomes['Failures'] = yearly_outcomes['Failures'].astype(int)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(x=yearly_outcomes['Year'], y=yearly_outcomes['Successes'], name='Successes', marker_color='#2ecc71')
            )
            fig.add_trace(
                go.Bar(x=yearly_outcomes['Year'], y=yearly_outcomes['Failures'], name='Failures', marker_color='#e74c3c')
            )
            fig.update_layout(
                title="Successes vs Failures by Year",
                barmode='group',
                margin=dict(t=40, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis_title="Missions",
                xaxis_title="Year"
            )
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
        else:
            st.info("No data available for outcomes chart.")

    # Data table
    st.subheader(f"Data ({len(data):,} missions)")
    show_price = st.checkbox("Show Mission Cost", value=True)
    if len(data) > 0:
        columns = ['Mission', 'Company', 'Date', 'Rocket', 'Location', 'MissionStatus']
        if show_price:
            columns.append('Price')
        display = data[columns].copy()
        display['Date'] = display['Date'].dt.strftime('%Y-%m-%d')
        if show_price:
            # Convert to numeric millions for proper sorting, keep NaN for missing
            display['Price'] = pd.to_numeric(display['Price'], errors='coerce')
            column_config = {
                "Price": st.column_config.NumberColumn(
                    "Price ($M)",
                    format="$%.1fM"
                )
            }
            st.dataframe(display.sort_values('Date', ascending=False), height=400, hide_index=True, column_config=column_config)
        else:
            st.dataframe(display.sort_values('Date', ascending=False), height=400, hide_index=True)
    else:
        columns = ['Mission', 'Company', 'Date', 'Rocket', 'Location', 'MissionStatus']
        if show_price:
            columns.append('Price')
        st.dataframe(pd.DataFrame(columns=columns), height=100, hide_index=True)


if __name__ == "__main__":
    main()
