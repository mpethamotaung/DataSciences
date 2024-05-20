from django.shortcuts import render
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import calendar
from .forms import CustomerForm

def index(request):
    form = CustomerForm()
    return render(request, 'index.html', {'form': form})

def submit(request):
    plot_div = None
    customer_info = None  # Initialize customer_info variable
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('excelFile')
            if excel_file:
                df = pd.read_excel(excel_file)
                if {'Month', 'Income', 'Expenses'}.issubset(df.columns):
                    # Process the data and generate Plotly graph
                    months_order = list(calendar.month_abbr)[1:]
                    df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)
                    df_monthly = df.groupby('Month').sum().reset_index()
                    trace1 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Income'], mode='lines', name='Income')
                    trace2 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Expenses'], mode='lines', name='Expenses')
                    data = [trace1, trace2]
                    layout = go.Layout(title=f'Monthly Income & Expenses', xaxis=dict(title='Month'), yaxis=dict(title='Amount'))
                    fig = go.Figure(data=data, layout=layout)
                    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                    # Get customer information from the form
                    customer_info = form.cleaned_data
                    return render(request, 'success.html', {'plot_div': plot_div, 'customer_info': customer_info})
                else:
                    error_message = "One or more required columns (Month, Income, Expenses) are missing in the uploaded Excel file."
                    return render(request, 'error.html', {'error_message': error_message})
            else:
                error_message = "No Excel file uploaded. Please select a file and try again."
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = CustomerForm()
    return render(request, 'index.html', {'form': form, 'plot_div': plot_div})


