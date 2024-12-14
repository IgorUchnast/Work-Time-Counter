from trello_data.get_trello_data import get_trello_data, get_trello_cards
from models.models import Employee, Project, ProjectMember, Task, TaskAssignment
from datetime import date
from db.db_configuration import db
import random


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


def save_trello_lists(board_id):
    board_lists = get_trello_data(board_id=board_id, data_type='lists') 
    
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
                

def save_trello_cards(list_id):
    trello_cards = get_trello_cards(list_id=list_id) 
    task = Task.query.filter_by(description=list_id).first()
    if task:
        # task_id = task.task_id
        for card in trello_cards:
            task_assignment = TaskAssignment.query.filter_by(trello_id=card["id"]).first()
            if not task_assignment:
                task_members = card["idMembers"]
                if task_members:
                    for employee_id in task_members: 
                        employees = Employee.query.all()
                        for employee in employees:
                            trello_id = employee.email.split('_')[-1].split('@')[0]
                            if employee_id == trello_id:
                                task_assignment = TaskAssignment(
                                    task_id=task.task_id,
                                    name=card['name'],
                                    employee_id= employee.employee_id,
                                    start_date=date.today(),
                                    trello_id=card["id"],
                                    description=card["desc"],
                                )
                                db.session.add(task_assignment)
                    db.session.commit()
                else:
                    task_assignment = TaskAssignment(
                        task_id=task.task_id,
                        name=card['name'],
                        employee_id= None,
                        start_date=date.today(),
                        trello_id=card["id"],
                        description=card["desc"],
                    )
                    db.session.add(task_assignment)
                db.session.commit()

