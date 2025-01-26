from db.db_configuration import db
from datetime import datetime
# MODELE DANYCH

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    position = db.Column(db.String, nullable=False)
    
    # projects = db.relationship('Project', backref='leader', lazy=True)

    project_memberships = db.relationship('ProjectMember', backref='employee', lazy=True)
    task_assignments = db.relationship('TaskAssignment', backref='employee', lazy=True)
    meeting_attendances = db.relationship('MeetingAttendance', backref='employee', lazy=True)
    work_summary = db.relationship('WorkSummary', backref='employee', lazy=True)


class ProjectMember(db.Model):
    __tablename__ = 'project_member'
    project_member_id =db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    role = db.Column(db.String, nullable=False)
    hours_worked = db.Column(db.Numeric, nullable=True)

    leader = db.relationship('Project', backref = 'project_member',foreign_keys=[project_id], lazy=True)

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    # end_date = db.Column(db.Date, nullable=True)
    # leader_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    leader_id = db.Column(db.Integer, db.ForeignKey('project_member.employee_id'), nullable=False)
    
    # members = db.relationship('ProjectMember', backref='project', lazy=True)
    members = db.relationship('ProjectMember', backref='project', foreign_keys=[ProjectMember.project_id], lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)
    meetings = db.relationship('Meeting', backref='project', lazy=True)



class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False) 
    # end_date = db.Column(db.Date, nullable=True)
    
    assignments = db.relationship('TaskAssignment', backref='task', lazy=True)


class TaskAssignment(db.Model):
    __tablename__ = 'task_assignment'
    assignment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    # Added for test 
    # **********
    description = db.Column(db.Text, nullable=True)
    trello_id = db.Column(db.Text, nullable=True)
    # trello_id = db.Column(db.Text, nullable=True, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    # **********
    # hours_spent = db.Column(db.Numeric, nullable=True)
    start_date = db.Column(db.Date, nullable=False)


class Meeting(db.Model):
    __tablename__ = 'meeting'
    meeting_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Numeric, nullable=True)
    location = db.Column(db.String, nullable=True)
    
    attendances = db.relationship('MeetingAttendance', backref='meeting', lazy=True)


class MeetingAttendance(db.Model):
    __tablename__ = 'meeting_attendance'
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    duration = db.Column(db.Numeric, nullable=True)


class WorkSummary(db.Model):
    __tablename__ = 'work_summary'
    worksummary_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task_assignment.assignment_id'), nullable=False)
    work_time = db.Column(db.Numeric, nullable=True)
    break_time = db.Column(db.Numeric, nullable=True)
    # task_start = db.Column(db.DateTime, default=datetime.now, nullable=True)
    # task_stop = db.Column(db.DateTime, default=datetime.now, nullable=True)
    date = db.Column(db.Date, default=datetime.utcnow)

class TaskStatus(db.Model):
    __tablename__ = 'task_status'
    task_status_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task_assignment.assignment_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    task_start = db.Column(db.DateTime, nullable=True)
    task_stop = db.Column(db.DateTime, nullable=True)

    def __init__(self, task_id, employee_id, task_start=None, task_stop=None):
        self.task_id = task_id
        self.employee_id = employee_id
        self.task_start = task_start
        self.task_stop = task_stop