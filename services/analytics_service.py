import pandas as pd
import numpy as np
import io
import csv
from models.task import Task

def generate_stats(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    if not tasks:
        return {
            "total_tasks": 0, "completed_tasks": 0, "pending_tasks": 0,
            "completion_percentage": 0, "high_priority_count": 0
        }

    df = pd.DataFrame([{'status': t.status, 'priority': t.priority} for t in tasks])
    
    total = len(df)
    completed = int(np.sum(df['status'] == 'Completed'))
    pending = int(np.sum(df['status'] == 'Pending'))
    comp_pct = round((completed / total) * 100, 2)
    high_pri = int(np.sum(df['priority'] == 'High'))

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": comp_pct,
        "high_priority_count": high_pri
    }

def export_tasks_csv(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Title', 'Description', 'Priority', 'Status', 'Created Date', 'Due Date'])
    for t in tasks:
        writer.writerow([t.id, t.title, t.description, t.priority, t.status, t.created_date, t.due_date])
    
    return output.getvalue()

import matplotlib.pyplot as plt
import os

def generate_trend_chart(user_id, static_folder):
    tasks = Task.query.filter_by(user_id=user_id).all()
    if not tasks:
        return None
    
    df = pd.DataFrame([{'date': t.created_date.date()} for t in tasks])
    trend = df.groupby('date').size()
    
    plt.figure(figsize=(10, 4))
    plt.plot(trend.index, trend.values, marker='o', linestyle='-', color='#007bff')
    plt.title('Task Creation Trend', color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Tasks', color='white')
    plt.grid(True, alpha=0.1)
    
    # Save with dark background
    plt.gcf().set_facecolor('#1e1e1e')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    
    chart_path = os.path.join(static_folder, 'images', f'trend_{user_id}.png')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()
    return f'images/trend_{user_id}.png'
