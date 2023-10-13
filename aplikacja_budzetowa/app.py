from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import csv

app = Flask(__name__)

budget = 0
expenses = []

@app.route('/')
def index():
    return render_template('index1.html', budget=budget, expenses=expenses)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    global budget
    new_budget = request.form.get('budget')
    budget = float(new_budget) if new_budget else 0
    session['budget'] = budget
    return redirect('/')

app.secret_key = 'twoj_tajny_klucz'

@app.route('/add_expense', methods=['POST'])
def add_expense():
    expense_name = request.form['expense_name']
    expense_amount = float(request.form['expense_amount'])
    paid = False
    expenses.append({'name': expense_name, 'amount': expense_amount, 'paid': paid})
    return redirect(url_for('index'))

@app.route('/mark_paid/<int:expense_index>')
def mark_paid(expense_index):
    global budget
    expense = expenses[expense_index]
    if not expense['paid']:
        expense['paid'] = True
        budget -= expense['amount']
    return redirect(url_for('index'))

@app.route('/generate_report')
def generate_report():
    budzet = session.get('budget', 0.0)
        
    report_data = [
        ['Nazwa wydatku', 'Kwota', 'Czy Opłacone?'],
    ]
    
    total_paid = 0
    total_unpaid = 0

    for expense in expenses:
        name = expense['name']
        amount = expense['amount']
        paid = expense['paid']
        
        if paid:
            total_paid += amount
        else:
            total_unpaid += amount
        
        report_data.append([name, amount, 'Tak' if paid else 'Nie'])

    remaining_budget = budzet - total_paid
    
    report_data.append(['', '', ''])
    report_data.insert(0,['Początkowy budżet', budzet, ''])
    report_data.append(['', '', ''])
    report_data.append(['Pozostało w budżecie', remaining_budget, ''])
    report_data.append(['', '', ''])
    report_data.append(['Całkowity koszt uiszczonych opłat', total_paid, ''])
    report_data.append(['Pozostało do zapłaty', total_unpaid, ''])

    with open('C:/Kodilla/kurs_python/Cwiczenie_9_4/aplikacja_budzetowa/budget_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(report_data)

    return redirect('/')
if __name__ == '__main__':
    app.run()
