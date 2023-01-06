import json
import datetime
import plotly.express as px
import pandas as pd

def plot_posting_frequency(days=365):
    # Load the JSON file
    with open('posts.json', 'r') as f:
        data = json.load(f)

    # Get the current date
    now = datetime.datetime.now()

    # Filter the data to only include posts from the past year
    filtered_data = [post for post in data if (now - datetime.datetime.fromisoformat(post['discovered'])).days < days]

    # Extract the group names and timestamps into separate lists
    group_names = []
    timestamps = []
    for post in filtered_data:
        group_names.append(post['group_name'])
        timestamps.append(post['discovered'])

    # Convert the lists into a Pandas dataframe
    df = pd.DataFrame({'group_name': group_names, 'timestamp': timestamps})

    # Convert the timestamps into a datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group and sort the data by the number of postings in each group
    df_sorted = df.groupby(['group_name', 'timestamp']).size().reset_index(name='count')
    df_sorted = df_sorted.sort_values(by='count', ascending=False)

    # Use Plotly's Heatmap plot to visualize the data
    fig = px.density_heatmap(df_sorted, x='timestamp', y='group_name', z='count', title='Posting Frequency by Group over Time',color_continuous_scale='Portland')
    fig.show()

plot_posting_frequency(90)
