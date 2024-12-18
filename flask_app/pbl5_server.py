from flask import Flask, jsonify, request, abort
from db.db_configuration import app, db
from models.models import Employee, Project, Task, TaskAssignment
from trello_data.fetch_trello_data import fetch_trello_employee, fetch_trello_lists, save_trello_projects


# # Endpoint obsługujący webhooki Trello
# @app.route('/webhook/trello', methods=['HEAD', 'POST'])
# def trello_webhook():
#     """
#     Endpoint obsługujący webhooki Trello.
#     """
#     if request.method == 'HEAD':
#         # Trello wysyła HEAD przy weryfikacji webhooka - zwracamy 200 OK
#         return '', 200

#     # Obsługa POST - odczyt danych przesłanych przez Trello
#     data = request.json
#     if not data or 'action' not in data:
#         return jsonify({"error": "Invalid payload"}), 400

#     action_type = data['action']['type']
#     print(f"Webhook received action: {action_type}")

#     # Przykładowa obsługa akcji Trello
#     if action_type in ['createCard', 'updateCard', 'deleteCard']:
#         print(f"Synchronizowanie zmian w Trello: {action_type}")
#         save_trello_projects()  # Aktualizacja projektów
#         fetch_trello_employee()  # Aktualizacja pracowników
#         fetch_trello_lists()  # Aktualizacja list zadań

#     return jsonify({"message": "Webhook handled"}), 200

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
        return jsonify([{"employee_id": employee.employee_id, "first_name": employee.first_name, "last_name": employee.last_name,
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

@app.route('/projects', methods=['GET'])
def get_projects(): 
    projects = Project.query.all()
    return jsonify([{
        "project_id": project.project_id, 
        "title": project.title, 
        "description": project.description, 
        "start_date": project.start_date,
        "leader_id" : project.leader_id,
    } for project in projects]), 200

@app.route('/projects', methods=['GET'])
def get_task_assignments(): 
    projects = Project.query.all()
    return jsonify([{
        "project_id": project.project_id, 
        "title": project.title, 
        "description": project.description, 
        "start_date": project.start_date,
        "leader_id" : project.leader_id,
    } for project in projects]), 200

# TO NIE DZIAŁA
# @app.route('/project/<int:project_id>/task/<int:task_id>/assignments', methods=['GET'])
# def get_project_members(project_id, task_id):
#     project = Project.query.get_or_404(project_id)
#     task = Task.query.get_or_404(task_id)
#     task_assignments = []
#     # task_assigmnets = TaskAssignment.query.get_or_404()
#     for task_assignment in task.assignments:
#         assignments = TaskAssignment.query.filter_by(task_id=task_assignment.task_id).first()
#         for assignment in assignments:
#             task_assignments.append({
#                 "task_id": assignment.task_id,
#                 'employee_id': assignment.employee_id,
#                 'description': assignment.description,
#                 'name': assignment.name,
#                 'start_date': assignment.start_date,
#             })
#     return jsonify(task_assignments)

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
    # db.drop_all() 
    db.create_all()

    save_trello_projects()
    fetch_trello_employee()
    fetch_trello_lists()
    
    
    

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