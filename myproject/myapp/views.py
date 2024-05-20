# views.py
from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

import calendar

def index(request):
    form = CustomerForm()
    return render(request, 'index.html', {'form': form})

def submit(request):
    if request.method == 'POST':
        # Handle CustomerForm submission
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()  # Save the form data to the database

            # Handle file upload
            excel_file = request.FILES.get('excelFile')
            if excel_file:
                df = pd.read_excel(excel_file)
                if {'Month', 'Income', 'Expenses'}.issubset(df.columns):
                    months_order = list(calendar.month_abbr)[1:]
                    df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)
                    df_monthly = df.groupby('Month').sum().reset_index()

                    trace1 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Income'], mode='lines', name='Income')
                    trace2 = go.Scatter(x=df_monthly['Month'], y=df_monthly['Expenses'], mode='lines', name='Expenses')
                    data = [trace1, trace2]

                    layout = go.Layout(title=f'Monthly Income & Expenses', xaxis=dict(title='Month'), yaxis=dict(title='Amount'))
                    fig = go.Figure(data=data, layout=layout)
                    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

                    # Get the latest saved customer
                    latest_customer = Customer.objects.latest('id')

                    return render(request, 'success.html', {'plot_div': plot_div, 'customer': latest_customer})
                else:
                    error_message = "One or more required columns (Month, Income, Expenses) are missing in the uploaded Excel file."
                    return render(request, 'error.html', {'error_message': error_message})

        # If form submission or file upload fails, re-render the index page with form errors
        form = CustomerForm(request.POST)
        return render(request, 'index.html', {'form': form})

    # If the request method is not POST, redirect to the index page
    return redirect('index')

def success(request):
    if 'customer' in request.session:  # Check if customer information is available in session
        customer = request.session.pop('customer')  # Get customer information from session
    else:
        customer = None

    return render(request, 'success.html', {'customer': customer})
