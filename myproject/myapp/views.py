from django.shortcuts import render


import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

import calendar


def index(request):
    return render(request, 'index.html')


def submit(request):
    if request.method == 'POST':

        # Extract uploaded Excel file
        excel_file = request.FILES.get('excelFile')

        if excel_file:

            
            # Read Excel file and process data
            df = pd.read_excel(excel_file)

            # Process data to calculate monthly income and expenditure
            if {'Month', 'Income', 'Expenses'}.issubset(df.columns):  # Check if required columns exist

                # Sort months in proper order
                months_order = list(calendar.month_abbr)[1:]
                df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)

                # Group by month and sum the income and expenses
                df_monthly = df.groupby('Month').sum().reset_index()  # Reset index for Plotly

                # Create Plotly traces
                trace1 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Income'], mode='lines', name='Income')
                trace2 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Expenses'], mode='lines', name='Expenses')
                data = [trace1, trace2]

                # Layout
                layout = go.Layout(title=f'Monthly Income & Expenses' , xaxis=dict(title='Month'), yaxis=dict(title='Amount'))

                # Create Plotly figure
                fig = go.Figure(data=data, layout=layout)

                # Convert Plotly figure to HTML
                plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                return render(request, 'success.html', {'plot_div': plot_div})
            else:
                error_message = "One or more required columns (Month, Income, Expenses) are missing in the uploaded Excel file."
                return render(request, 'error.html', {'error_message': error_message})
    return render(request, 'index.html')

