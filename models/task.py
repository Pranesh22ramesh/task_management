from datetime import datetime
from models.user import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='Medium') # High, Medium, Low
    status = db.Column(db.String(20), default='Pending') # Pending, Completed
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_date': self.created_date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'is_overdue': self.due_date < datetime.utcnow() if (self.due_date and self.status == 'Pending') else False,
            'user_id': self.user_id
        }
