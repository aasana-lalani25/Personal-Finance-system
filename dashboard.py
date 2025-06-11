import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

conversion_rate = 10

# Initialize the Dash app
app = Dash(__name__)
app.title = "Personal Finance Dashboard"

CARD_STYLE = {
    'border-radius': '10px',
    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
    'padding': '20px',
    'margin': '10px',
    'text-align': 'center',
    'font-family': 'Poppins, sans-serif',
}

TEXT_STYLE = {'font-family': 'Poppins, sans-serif'}

app.layout = html.Div([
    html.H1("Personal Finance Dashboard", style={'text-align': 'center', 'color': '#4A90E2', 'font-family': 'Poppins, sans-serif'}),
    
    # File upload section
    html.Div([
        html.H3("Upload Your Finance CSV File:", style=TEXT_STYLE),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files', style={'color': '#007BFF', 'text-decoration': 'underline'}),
            ]),
            style={
                'width': '50%',
                'margin': '10px auto',
                'padding': '20px',
                'border-width': '2px',
                'border-style': 'dashed',
                'border-color': '#007BFF',
                'text-align': 'center',
                'border-radius': '10px',
                'font-family': 'Poppins, sans-serif',
            },
            multiple=False
        ),
    ]),
    
    # Summary cards
    html.Div(id='summary-cards', style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap'}),
    
    # Graphs
    html.Div(id='graphs', style={'margin': '20px'}),
    
    # Suggestions
    html.Div(id='suggestions', style={'padding': '20px', 'margin': '10px', 'background-color': '#f9f9f9', 'border': '1px solid #ddd', 'border-radius': '10px', 'font-family': 'Poppins, sans-serif'}),
])

@app.callback(
    [Output('summary-cards', 'children'),
     Output('graphs', 'children'),
     Output('suggestions', 'children')],
    [Input('upload-data', 'contents')]
)
def update_dashboard(contents):
    if contents is None:
        return [], [], html.P("Please upload a CSV file to view suggestions.", style=TEXT_STYLE)

    # Read and process data
    data = pd.read_csv(r"C:\Users\Payal Makwana\Downloads\reliable_finance_data.csv")
    
    monthly_data = data.groupby('Month')[['Income', 'Expenses']].sum().reset_index()
    monthly_data['Income'] *= conversion_rate
    monthly_data['Expenses'] *= conversion_rate
    monthly_data['Savings'] = monthly_data['Income'] - monthly_data['Expenses']
    
    total_income = monthly_data['Income'].sum()
    total_expenses = monthly_data['Expenses'].sum()
    total_savings = total_income - total_expenses
    savings_percentage = (total_savings / total_income) * 100
    
    category_data = data.groupby('Category')['Amount'].sum().reset_index()
    category_data['Amount'] *= conversion_rate
    
    # Summary cards
    summary_cards = [
        html.Div([
            html.H3(f"Total Income: ₹{total_income:,.2f}", style={'color': '#28A745'}),
        ], style={**CARD_STYLE, 'background-color': '#DFF2E3'}),
        
        html.Div([
            html.H3(f"Total Expenses: ₹{total_expenses:,.2f}", style={'color': '#DC3545'}),
        ], style={**CARD_STYLE, 'background-color': '#F8D7DA'}),
        
        html.Div([
            html.H3(f"Total Savings: ₹{total_savings:,.2f} ({savings_percentage:.2f}% of income)", style={'color': '#007BFF'}),
        ], style={**CARD_STYLE, 'background-color': '#D1ECF1'}),
    ]
    
    # Graphs
    graphs = html.Div([
        html.Div([
            dcc.Graph(
                id='monthly-overview',
                figure=px.bar(monthly_data, x='Month', y=['Income', 'Expenses'],
                              barmode='group', title="Monthly Overview (Income vs Expenses in ₹)")
                .update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2))
            )
        ]),
        
        html.Div([
            dcc.Graph(
                id='expense-categories',
                figure=px.pie(category_data, values='Amount', names='Category', title="Expense Categories in ₹")
                .update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2))
            )
        ]),

        html.Div([
            dcc.Graph(
                id='savings-trend',
                figure=px.line(monthly_data, x='Month', y='Savings', title="Savings Trend (in ₹)")
                .update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2))
            )
        ]),
    ])
    
    # Suggestions
    suggestions = html.Div([
        html.H2("Suggestions", style={'color': '#6C757D'}),
        html.P(f"1. Your total savings of ₹{total_savings:,.2f} is {savings_percentage:.2f}% of your income. "
               "Consider maintaining at least 20-30% savings.", style=TEXT_STYLE),
        html.P("2. Review categories like Rent, Utilities, and Groceries for cost-cutting opportunities.", style=TEXT_STYLE),
        html.P("3. Consider reducing discretionary spending on categories like Entertainment.", style=TEXT_STYLE),
        html.P("4. Aim to save more by setting fixed budgets for high-spending categories.", style=TEXT_STYLE),
    ])
    
    return summary_cards, graphs, suggestions

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
