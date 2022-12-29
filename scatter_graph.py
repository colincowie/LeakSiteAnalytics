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


    # Convert the lists into a Pandas dataframe
    df = pd.DataFrame({'group_name': group_names, 'timestamp': timestamps})

    # Convert the timestamps into a datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Use Plotly's Scatter plot to visualize the data
    fig = px.scatter(df, x='timestamp', y='group_name', color='group_name', title='Posting Frequency by Group over Time', color_continuous_scale='Portland')
    fig.show()

plot_posting_frequency()
