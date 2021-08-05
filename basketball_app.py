import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


@st.cache
def load_data(year: int, stage: str) -> pd.DataFrame:
    """
    Web scraping of NBA player stats

    Args:
        year (int):
        stage (str):

    Returns:
        pd.DataFrame
    """
    url = ''.join(('https://www.basketball-reference.com/', stage, '/NBA_', str(year), '_per_game.html'))
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
    # string <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
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


# PAGE LAYOUT - Page extends to full width
st.set_page_config(layout="wide")

# --- SIDEBAR --- #
# Sidebar - Year selection
st.sidebar.header('User Input Features')
selected_year_int = st.sidebar.selectbox(label='Year', options=list(reversed(range(1950, 2022))))

# Sidebar - Stage
radio_input = st.sidebar.radio('Season/Play-off', ['Season', 'Play-off'])
if radio_input == 'Season':
    stage_str = 'leagues'
else:
    stage_str = 'playoffs'

# Load data with selected Year
player_stats_df = load_data(selected_year_int, stage_str)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats_df.Tm.unique())
container_team = st.sidebar.beta_container()
all_teams = st.sidebar.checkbox("Select all teams", value=True)

if all_teams:
    selected_team = container_team.multiselect(label='Team', options=sorted_unique_team, default=sorted_unique_team,
                                               help='Display selected teams stats')
else:
    selected_team = container_team.multiselect(label='Team', options=sorted_unique_team,
                                               help='Display selected teams stats')

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
container_pos = st.sidebar.beta_container()
all_pos = st.sidebar.checkbox("Select all positions", value=True)

if all_pos:
    selected_pos = container_pos.multiselect('Position', unique_pos, unique_pos)
else:
    selected_pos = container_pos.multiselect('Position', unique_pos)

# Filtering data
df_selected_team_and_position = player_stats_df[(player_stats_df.Tm.isin(selected_team)) &
                                                (player_stats_df.Pos.isin(selected_pos))]

# --- MAIN --- #
# Main - title and description
st.title('NBA Player Stats Explorer')

about_expander = st.beta_expander("About")
about_expander.markdown("""

#### How to use? 
Use the side panel to choose the following:
* Year
* Stats from: Regular season or Play-offs
* Players from Teams 
* Players from Positions

######
#### Additional info:
* Data source: This app performs simple web-scraping from [Basketball-reference.com](https://www.basketball-reference.com/).
* Credit: Base app idea and content adapted from [Streamlit tutorial](https://youtu.be/xiBXspqs0dk) created by 
  [Data Professor](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q) 
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
