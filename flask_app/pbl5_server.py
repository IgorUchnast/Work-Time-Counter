from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config.api_key import API_KEY, TOKEN, BASE_URL, BOARD_ID, WORK_SPACE
import requests
from datetime import date
import random
import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    # end_date = db.Column(db.Date, nullable=True)
    
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
            # 'end_date': project.end_date,
            'leader_id': project.leader_id,
        })
    
    # Zwrócenie wyników w formacie JSON
    return jsonify(projects)



# ************************************************************************************************************

def get_boards_in_workspace(workspace_id): 
    url = f"{BASE_URL}/organizations/{workspace_id}/boards"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None

def get_trello_data(board_id, data_type):

    url = f"{BASE_URL}/boards/{board_id}/{data_type}"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    # Sprawdzenie, czy zapytanie się powiodło
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None


def save_trello_projects():
    boards = get_boards_in_workspace(WORK_SPACE)

    if boards:
        for board_id in range(len(boards)):
            description = boards[board_id].get('description')
            if not description:
                description = f"{boards[board_id]['id']}"
            board = Project.query.filter_by(description=description).first()
            if not board:
                board = Project(
                    title = boards[board_id]['name'],
                    description = boards[board_id]['id'],
                    start_date = date.today(),
                    leader_id = random.choice([1, 2])
                )
                db.session.add(board)
                db.session.commit()

def fetch_trello_lists():
    boards = get_boards_in_workspace(WORK_SPACE)
    if boards:
        for board in boards:
            board_id = board['id']
            lists = get_trello_data(board_id=board_id, data_type='lists')
            if lists:
                for list in lists:
                    save_trello_lists(board_id=board_id)

def fetch_trello_employee():
    boards = get_boards_in_workspace(WORK_SPACE)
    if boards:
        for board in boards:
            board_id = board['id']
            members = get_trello_data(board_id=board_id, data_type='members')
            if members:
                for member in members:
                    save_trello_employee(board_id=board_id)

def fetch_trello_project_members():
    boards = get_boards_in_workspace(WORK_SPACE)
    if boards:
        for board in boards:
            board_id = board['id']
            members = get_trello_data(board_id, data_type='members')
            if members:
                for member in members:
                    save_project_members(board_id=board_id)



def save_trello_employee(board_id):
    board_members = get_trello_data(board_id, data_type='members') 
    
    if board_members:
        for member in board_members:
            email = member.get('email')  # Pobierz email, jeśli jest dostępny
            if not email:  # Jeśli brak, ustaw tymczasowy email
                email = f"{member['fullName'].split()[0]}_{''.join(member['fullName'].split()[1:])}_{member['id']}@company.com"
                
            employee = Employee.query.filter_by(email=email).first()
            if not employee:
                employee = Employee(
                    first_name=member['fullName'].split()[0],
                    last_name=" ".join(member['fullName'].split()[1:]),
                    email=email,
                    position= random.choice(["Software Developer", "Mobile-App Developer", "Web-App Developer", "Data Analyss"])
                )
                db.session.add(employee)
                db.session.commit()
            # Powiąż pracownika z aktualnym projektem (board_id)
            project = Project.query.filter_by(description=board_id).first()
            if project:
                # Sprawdź, czy relacja już istnieje
                project_member = ProjectMember.query.filter_by(
                    project_id=project.project_id, 
                    employee_id=employee.employee_id
                ).first()
                
                if not project_member:
                    project_member = ProjectMember(
                        project_id=project.project_id,
                        employee_id=employee.employee_id,
                        role=employee.position,
                        hours_worked=random.choice([1, 2, 3, 1.5, 2.5, 3.5])
                    )
                    db.session.add(project_member)
                    db.session.commit()

def save_project_members(board_id):
    # board_members = get_trello_data(board_id, data_type='members') 
    projects = Project.query.all()
    for project in projects:
        # if project.description == board_id:
        if project.description.strip() == board_id.strip():
            employees = Employee.query.all()
            # employees = Employee.query.filter_by(Employee.email).first()
            # ************************************************************************************
            # Wszyscy pracownicy są dodawaniu do projektów, jeśli nie są doani do tabeli projkect_member, nawet jeśl nie nalezą do danego projektu
            # ************************************************************************************
            for employee in employees:
                project_member = ProjectMember.query.filter_by(employee_id=employee.employee_id,project_id=project.project_id).first()
                if not project_member:
                    project_member = ProjectMember(
                        project_id= project.project_id,
                        employee_id=employee.employee_id,
                        role=employee.position,
                        hours_worked= random.choice([1,2,3,1.5,2.5,3.5])
                    )
                    try:
                        db.session.add(project_member)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Błąd podczas zapisywania członka projektu: {e}") 

def save_trello_lists(board_id):
    board_lists = get_trello_data(board_id, data_type='lists') 
    
    if board_lists:
        for list in board_lists:
            list_id = list.get('id')
            if not list_id:
                list_id = None
            project = Project.query.filter_by(description=board_id).first()
            if project:
                id = project.project_id
            task = Task.query.filter_by(description=list_id).first()
            if not task:
                task = Task(
                    project_id= id,
                    title=list['name'],
                    description=list['id'],
                    start_date=date.today(),
                    # end_date= date.today() if list.get('closed') else '0000-00-00'
                )
                db.session.add(task)
                db.session.commit()

# INICJALIZACJA BAZY DANYCH
with app.app_context():
    db.drop_all()
    db.create_all()
    # add_trello_boards_to_projects()
    # add_trello_employee(BOARD_ID)
    save_trello_projects()
    fetch_trello_employee()
    fetch_trello_lists()
    # fetch_trello_project_members()
    
    
    

if __name__ == '__main__':
    app.run(debug=True)

# backref
# backref tworzy automatyczny, dwukierunkowy dostęp między powiązanymi obiektami, 
# dodając atrybut odwrotny (ang. back-reference) w obiekcie po drugiej stronie relacji. 
# backref to uproszczenie, które łączy obie strony relacji bez potrzeby definiowania ich osobno.

# LAZY
# Lazy loading pozwala zmniejszyć liczbę danych pobieranych w momencie zapytania o obiekt główny (np. Employee). 
# Dopiero gdy faktycznie potrzebujemy dostępu do powiązanych danych, SQLAlchemy pobiera je z bazy.