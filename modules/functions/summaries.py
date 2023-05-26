from modules.database.database_connect import DatabaseConnector
import datetime 
from calendar import monthrange


def get_user_currency(username):
    db = DatabaseConnector()
    query = f"SELECT currency FROM users WHERE username='{username}'"
    
    return db.select_data(query, 'one')[0]


def get_daily_summary(username, day='now'):
    db = DatabaseConnector()
    if day == 'now':
        query = f"SELECT e.amount, c.name from expenses AS e JOIN users AS u ON e.user_id=u.id JOIN categories AS " \
                f"c ON e.category_id=c.id WHERE u.username='{username}'AND e.add_date=CURRENT_DATE"
    else:
        query = f"SELECT e.amount, c.name from expenses AS e JOIN users AS u ON e.user_id=u.id JOIN categories AS " \
                f"c ON e.category_id=c.id WHERE u.username='{username}'AND e.add_date=TO_DATE('{day}', 'DD-MM-YYYY')"
    
    results = db.select_data(query)

    summary = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}
    for r in results:
        if r[1] == 'Entertainment':
            summary['Entertainment'] += float(r[0])
        elif r[1] == 'Shopping':
            summary['Shopping'] += float(r[0])
        elif r[1] == 'Bills':
            summary['Bills'] += float(r[0])
        elif r[1] == 'Subscriptions':
            summary['Subscriptions'] += float(r[0])
        else:
            summary['Other'] += float(r[0])

    return summary, results


def get_month_summary(username, month='now'):
    db = DatabaseConnector()
    if month == 'now':
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        query = f"SELECT e.amount, c.name, EXTRACT(MONTH FROM add_date) from expenses AS e JOIN " \
                f"users AS u ON e.user_id=u.id JOIN categories AS c ON e.category_id=c.id " \
                f"WHERE u.username='{username}' AND EXTRACT(MONTH FROM add_date) = {current_month} " \
                f"AND EXTRACT(YEAR FROM add_date) = {current_year}"
    else:

        query = f"SELECT e.amount, c.name, EXTRACT(MONTH FROM add_date) from expenses AS e JOIN " \
                f"users AS u ON e.user_id=u.id JOIN categories AS c ON e.category_id=c.id " \
                f"WHERE u.username='{username}' AND EXTRACT(MONTH FROM add_date) = {int(month.split('-')[0])} " \
                f"AND EXTRACT(YEAR FROM add_date) = {int(month.split('-')[1])}"

    month_results = db.select_data(query)
    month_summary = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}
    
    for r in month_results:
        if r[1] == 'Entertainment':
            month_summary['Entertainment'] += float(r[0])
        elif r[1] == 'Shopping':
            month_summary['Shopping'] += float(r[0])
        elif r[1] == 'Bills':
            month_summary['Bills'] += float(r[0])
        elif r[1] == 'Subscriptions':
            month_summary['Subscriptions'] += float(r[0])
        else:
            month_summary['Other'] += float(r[0])

    return month_summary, month_results


def generate_month_graph_data(username):
    db = DatabaseConnector()
    current_month = datetime.datetime.now().month  
    current_year = datetime.datetime.now().year
    query = f"SELECT e.amount, c.name, EXTRACT(DAY FROM e.add_date) as day from expenses AS e " \
            f"JOIN users AS u ON e.user_id=u.id JOIN categories AS c ON e.category_id=c.id " \
            f"WHERE u.username='{username}' AND EXTRACT(MONTH FROM add_date) = {current_month} " \
            f"AND EXTRACT(YEAR FROM add_date) = {current_year}"

    days_in_month = monthrange(current_year, current_month)[1]

    month_results = db.select_data(query)

    month_graph_data = {}
    for i in range(1, days_in_month+1):
        month_graph_data[i] = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}

    for r in month_results:
        for m in month_graph_data:
            if int(r[2]) == m:
                if r[1] == 'Entertainment':
                    month_graph_data[m]['Entertainment'] += float(r[0])
                elif r[1] == 'Shopping':
                    month_graph_data[m]['Shopping'] += float(r[0])
                elif r[1] == 'Bills':
                    month_graph_data[m]['Bills'] += float(r[0])
                elif r[1] == 'Subscriptions':
                    month_graph_data[m]['Subscriptions'] += float(r[0])
                else:
                    month_graph_data[m]['Other'] += float(r[0])
    
    x = month_graph_data.keys()
    entertainment_list = []
    shopping_list = []
    bills_list = []
    subs_list = []
    other_list = []

    for i in month_graph_data:
        for k, v in month_graph_data[i].items():
            if k == 'Entertainment':
                entertainment_list.append(v)
            elif k == 'Shopping':
                shopping_list.append(v)
            elif k == 'Bills':
                bills_list.append(v)
            elif k == 'Subscriptions':
                subs_list.append(v)
            else:
                other_list.append(v)
    
    return x, days_in_month, entertainment_list, shopping_list, bills_list, subs_list, other_list
    

def sum_lists(*lists):
    result = []
    for i in range(len(lists[0])):
        total = 0
        for lst in lists:
            total += lst[i]
        result.append(total)

    return result


def get_spend_limit(username):
    db = DatabaseConnector()
    query = f"SELECT spend_limit FROM users WHERE username = '{username}'"
    
    return db.select_data(query, 'one')[0]