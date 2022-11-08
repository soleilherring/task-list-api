from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="task")

    def to_dict(self):

        return {
            "id": self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete": bool(self.completed_at)
        }

    @classmethod
    def from_dict(cls, task_data):
        
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task
        