from flask import Flask, jsonify, request
from db.db_configuration import app, db
from models.models import Employee, Project, Task, TaskAssignment
from trello_data.fetch_trello_data import fetch_trello_employee, fetch_trello_lists, save_trello_projects

@app.route('/employees', methods=['GET', 'POST'])
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



@app.route('/employee/<int:employee_id>/projects', methods=['GET'])
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

@app.route('/employee/<int:employee_id>/tasks', methods=['GET'])
def get_employee_task(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    tasks = []
    for task in employee.task_assignments:
        tasks.append({
            'task_id': task.task_id,
            'employee_id': task.employee_id,
            'name': task.name,
            'description': task.description,
            'start_date': task.start_date,
        })
    return jsonify(tasks)

@app.route('/projects/', methods=['GET'])
def get_projects(): 
    projects = Project.query.all()
    return jsonify([{
        "project_id": project.project_id, 
        "title": project.title, 
        "description": project.description, 
        "start_date": project.start_date,
        "leader_id" : project.leader_id,
    } for project in projects]), 200


@app.route('/project/<int:project_id>/members', methods=['GET'])
def get_project_members(project_id):
    project = Project.query.get_or_404(project_id)
    employees = []
    for project_member in project.members:
        employee = Employee.query.get(project_member.employee_id)
        employees.append({
            'employee_id': employee.employee_id, 
            'first_name': employee.first_name, 
            'last_name': employee.last_name, 
            'email': employee.email, 
            'position': employee.position, 
        })
    return jsonify(employees)

@app.route('/project/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = []
    for task in project.tasks:
        task_assigment = Task.query.all()
        tasks.append({
            'task_id': task.task_id,
            'project_id': task.project_id,
            'title': task.title,
            'description': task.description,
            'start_date': task.start_date,
        })
    return jsonify(tasks)
# ************************************************************************************************************

# INICJALIZACJA BAZY DANYCH
with app.app_context():
    db.drop_all()
    db.create_all()

    save_trello_projects()
    fetch_trello_employee()
    fetch_trello_lists()
    # fetch_trello_cards()
    # fetch_employee_tasks()
    # save_trello_cards()
    
    
    

if __name__ == '__main__':
    app.run(debug=True)

# ************************************************************************************************************

# backref
# backref tworzy automatyczny, dwukierunkowy dostęp między powiązanymi obiektami, 
# dodając atrybut odwrotny (ang. back-reference) w obiekcie po drugiej stronie relacji. 
# backref to uproszczenie, które łączy obie strony relacji bez potrzeby definiowania ich osobno.

# LAZY
# Lazy loading pozwala zmniejszyć liczbę danych pobieranych w momencie zapytania o obiekt główny (np. Employee). 
# Dopiero gdy faktycznie potrzebujemy dostępu do powiązanych danych, SQLAlchemy pobiera je z bazy.