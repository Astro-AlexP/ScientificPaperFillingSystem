from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

app = Dash(__name__)




if __name__ == '__main__':
    app.run(debug=True)