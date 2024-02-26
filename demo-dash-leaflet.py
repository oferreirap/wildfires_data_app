from dash import Dash, html, dcc, Input, Output
import dash_leaflet as dl
import pandas as pd

# Load the CSV file
df = pd.read_csv('https://raw.githubusercontent.com/oferreirap/wildfires_data_app/main/Data/modis_2022_Colombia.csv')
df = df.iloc[30190:]  # last day of 2022 (December 31)
# Function to determine the color of market based on brightness
def get_color(brightness):
    if brightness < 310:
        return 'blue'
    elif 310 <= brightness < 330:
        return 'purple'
    elif 330 <= brightness < 350:
        return 'orange'
    else:
        return 'yellow'

# Add a 'color' column to the dataframe based on the 'brightness' value
df['color'] = df['brightness'].apply(get_color)

# Initialize the Dash app
app = Dash()

# App layout
app.layout = html.Div([
    html.H1("Fires in Colombia"),
    dl.Map(style={'width': '1000px', 'height': '500px'}, center=[4.5709, -74.2973], zoom=5, children=[
        dl.TileLayer(),
        # Use list comprehension to create markers for each fire location
        dl.LayerGroup(
            [
                dl.CircleMarker(center=[row['latitude'], row['longitude']],
                                radius=5,
                                color=row['color'],
                                fill=True,
                                fillOpacity=0.7,
                                children=[
                                    dl.Tooltip(
                                        f"Brightness: {row['brightness']}")
                                ])
                for index, row in df.iterrows()
            ]
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
