import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


@st.cache
def load_data(year: int) -> pd.DataFrame:
    """
    Web scraping of NBA player stats

    Args:
        year (int):

    Returns:
        pd.DataFrame
    """
    url = ''.join(('https://www.basketball-reference.com/leagues/NBA_', str(year), '_per_game.html'))
    html = pd.read_html(url, header=0)
    df = html[0]
    # drop rows with recursive header values
    df = df.drop(df[df.Age == 'Age'].index)
    # convert to numeric all cols except string values
    cols = df.columns.drop(['Player', 'Pos', 'Tm'])
    df[cols] = df[cols].apply(pd.to_numeric)
    # fill missing data and remove indexing 'Rk' col
    df = df.fillna(0)
    df = df.drop(['Rk'], axis=1)
    return df


def download_csv_file_link(df: pd.DataFrame) -> str:
    """
    Generates a link allowing the data in a given panda dataframe to be downloaded

    Args:
        df(pd.DataFrame): data for selected year, team and position

    Returns:
        href str
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # string <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href


def generate_heatmap(df: pd.DataFrame):
    """
    Generates heatmap from DataFrame

    Args:
        df(pd.DataFrame): data for selected year, team and position

    Returns:

    """

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)


# --- SIDEBAR --- #
# Sidebar - Year selection
st.sidebar.header('User Input Features')
selected_year_int = st.sidebar.selectbox(label='Year', options=list(reversed(range(1950, 2022))))

# Load data with selected Year
player_stats_df = load_data(selected_year_int)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats_df.Tm.unique())
selected_team = st.sidebar.multiselect(label='Team', options=sorted_unique_team, default=sorted_unique_team,
                                       help='Display selected teams stats')

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team_and_position = player_stats_df[(player_stats_df.Tm.isin(selected_team)) &
                                                (player_stats_df.Pos.isin(selected_pos))]

# --- MAIN --- #
# Main - title and description
st.title('NBA Player Stats Explorer')
st.markdown("""
This app performs simple web-scraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# Main - Display Player Stats
st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimension: {str(df_selected_team_and_position.shape[0])} rows and '
         f'{str(df_selected_team_and_position.shape[1])} columns.')
st.dataframe(df_selected_team_and_position)

# Main - Download CSV file
st.markdown(download_csv_file_link(df_selected_team_and_position), unsafe_allow_html=True)

# Main - Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    generate_heatmap(df_selected_team_and_position)
