import json
import datetime
import plotly.express as px
import plotly.io as pio
import pandas as pd
import requests

def download_latest_data():
    print("[*] Downloading most recent RansomWatch data...")
    # Set the URL of the file to download
    url = 'https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the file to the current working directory
        with open('posts.json', 'w') as f:
            f.write(response.text)
    else:
        print('Failed to download file:', response.status_code)
    # Load the JSON file
    with open('posts.json', 'r') as f:
        data = json.load(f)
    return data

def run_data_viz(days_filter, data):
    print("[*] Creating plotly dashboards with a "+str(days_filter)+ " day filter")

    # Get the current date
    now = datetime.datetime.now()
    # Filter the data to only include posts from the past year
    filtered_data = [post for post in data if (now - datetime.datetime.fromisoformat(post['discovered'])).days < days_filter]

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

    # Use Plotly's Heatmap plot to create the density heatmap
    fig1 = px.density_heatmap(df_sorted, x='timestamp', y='group_name', z='count', title='Posting Frequency by group', template='plotly_dark')
    fig1.update_layout(font=dict(family='Roboto'))
    #fig1.show()
    filename = "density_heatmap_"+ str(days_filter)+".html"
    pio.write_html(fig1, file=filename)


    # Use Plotly's Scatter plot to create the scatter plot
    fig2 = px.scatter(df_sorted, x='timestamp', y='group_name', color='group_name', title='Posting Frequency by group', template='plotly_dark', color_continuous_scale='Plotly3')
    #fig2 = px.scatter(df_sorted, x='group_name', y='count', title='Posting Frequency by Group', template='plotly_dark')
    filename = "scatter_plot_"+ str(days_filter)+".html"
    pio.write_html(fig2, file=filename)
    #fig2.show()

    # Use Plotly's Bar plot to create the bar chart
    #fig4 = px.bar(df_sorted, x='group_name', y='count', color='count', title='Posting Frequency by Group', template='plotly_dark', color_continuous_scale='Portland')
    #fig4.show()

    # Group and sort the data by the number of postings in each group
    df_sorted = df.groupby('group_name').size().reset_index(name='count').sort_values(by='count', ascending=True)

    # Use Plotly's Pie plot to create the pie chart
    fig3 = px.pie(df_sorted, values='count', names='group_name', title='Posting Frequency by Group', template='plotly_dark')
    filename = "pie_chart_"+ str(days_filter)+".html"
    pio.write_html(fig3, file=filename)


    # Use Plotly's Scatter plot to visualize the data
    fig4 = px.bar(df_sorted, x='group_name', y='count', color='count', title='Posting Frequency by Group', color_continuous_scale='Portland', template='plotly_dark')
    filename = "bar_chart_"+ str(days_filter)+".html"
    pio.write_html(fig4, file=filename)
    print("[!] Finishing writing protly data to disk!")
    #fig3.show()

data = download_latest_data()
run_data_viz(7, data)
run_data_viz(14, data)
run_data_viz(30, data)
