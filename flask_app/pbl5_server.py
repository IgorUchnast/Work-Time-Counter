from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    work_station = db.relationship('WorkStation', backref='employee', uselist=False)


class ProjectMember(db.Model):
    __tablename__ = 'project_member'
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    role = db.Column(db.String, nullable=False)
    hours_worked = db.Column(db.Numeric, nullable=True)

    leader = db.relationship('Project', backref = 'project_member',foreign_keys=[project_id], lazy=True)

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    # leader_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    leader_id = db.Column(db.Integer, db.ForeignKey('project_member.employee_id'), nullable=False)
    
    # members = db.relationship('ProjectMember', backref='project', lazy=True)
    members = db.relationship('ProjectMember', backref='project', foreign_keys=[ProjectMember.project_id], lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)
    meetings = db.relationship('Meeting', backref='project', lazy=True)


# class ProjectMember(db.Model):
#     __tablename__ = 'project_member'
#     project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
#     role = db.Column(db.String, nullable=False)
#     hours_worked = db.Column(db.Numeric, nullable=True)

#     leader = db.relationship('Project', backref = 'project_member', lazy=True)


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    
    assignments = db.relationship('TaskAssignment', backref='task', lazy=True)


class TaskAssignment(db.Model):
    __tablename__ = 'task_assignment'
    assignment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    hours_spent = db.Column(db.Numeric, nullable=True)


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


class WorkStation(db.Model):
    __tablename__ = 'work_station'
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    work_time = db.Column(db.Numeric, nullable=True)
    break_time = db.Column(db.Numeric, nullable=True)


@app.route('/employee', methods=['GET', 'POST'])
def add_new_employee():
     if request.method == 'POST':
        # Dodawanie nowego użytkownika
        data = request.json
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            position=data['position'],
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee created"}), 201
     elif request.method == 'GET':
        # Pobieranie listy użytkowników
        employees = Employee.query.all()
        return jsonify([{"id": employee.employee_id, "first_name": employee.first_name, "last_name": employee.last_name,
                 "email": employee.email, "position": employee.position} for employee in employees]), 200


@app.route('/employee_projects/<int:employee_id>', methods=['GET'])
def get_employee_projects(employee_id):
    # Pobranie pracownika z bazy danych
    employee = Employee.query.get_or_404(employee_id)
    
    # Pobranie wszystkich projektów, w których pracownik jest członkiem
    projects = []
    for project_member in employee.project_memberships:
        project = Project.query.get(project_member.project_id)
        projects.append({
            'project_id': project.project_id,
            'title': project.title,
            'description': project.description,
            'start_date': project.start_date,
            'end_date': project.end_date
        })
    
    # Zwrócenie wyników w formacie JSON
    return jsonify(projects)


# backref
# backref tworzy automatyczny, dwukierunkowy dostęp między powiązanymi obiektami, 
# dodając atrybut odwrotny (ang. back-reference) w obiekcie po drugiej stronie relacji. 
# backref to uproszczenie, które łączy obie strony relacji bez potrzeby definiowania ich osobno.

# LAZY
# Lazy loading pozwala zmniejszyć liczbę danych pobieranych w momencie zapytania o obiekt główny (np. Employee). 
# Dopiero gdy faktycznie potrzebujemy dostępu do powiązanych danych, SQLAlchemy pobiera je z bazy.

# INICJALIZACJA BAZY DANYCH

# @app.before_first_request
# def create_tables():
#     db.create_all()
# Inicjalizacja bazy danych
with app.app_context():
    # db.drop_all()
    db.create_all()
    # Dodaj nowego pracownika
    # new_employee = Employee(
    #     first_name='Jan',
    #     last_name='Kowalski',
    #     email='jan.kowalski@example.com',
    #     position='Developer'
    # )
    
    # db.session.add(new_employee)
    # db.session.commit()

    # # Dodaj nowy projekt (jeśli nie istnieje)
    # new_project = Project(
    #     title='Projekt X',
    #     description='Impreza u Bartka',
    #     start_date=datetime.now().date()
    # )
    
    # db.session.add(new_project)
    # db.session.commit()

    # # Dodaj nową rolę dla pracownika w projekcie
    # new_project_member = ProjectMember(
    #     project_id=new_project.project_id,
    #     employee_id=new_employee.employee_id,
    #     role='Organizator Alko',
    #     hours_worked=0
    # )
    
    # db.session.add(new_project_member)
    # db.session.commit()

    # # Dodaj nowe zadanie dla pracownika w projekcie
    # new_task = Task(
    #     project_id=new_project.project_id,
    #     title='Zadanie 1',
    #     description='Zrobienie Imprezy X.',
    #     start_date=datetime.now().date(),
    #     end_date=None,  # lub datetime.now().date() + timedelta(days=7) dla daty końcowej
    #     # employee_id=new_employee.employee_id
    # )

    # db.session.add(new_task)
    # db.session.commit()

    # new_task_assignment = TaskAssignment(
    #     task_id=new_task.task_id,
    #     employee_id=new_employee.employee_id,
    #     hours_spent=2
    # )

    # db.session.add(new_task_assignment)
    # db.session.commit()

    

if __name__ == '__main__':
    app.run(debug=True)
