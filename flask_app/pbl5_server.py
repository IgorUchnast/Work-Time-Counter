from flask import Flask, jsonify, request, abort
from db.db_configuration import app, db
from models.models import Employee, Project, Task, TaskAssignment, WorkSummary
from trello_data.fetch_trello_data import fetch_trello_employee, fetch_trello_lists, save_trello_projects
from datetime import date

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

@app.route('/employee/<int:employee_id>/work_summary', methods=['GET', 'POST'])
def manage_work_station(employee_id):
    if request.method == 'GET':
        try:
            # Pobierz dane stanowiska pracy dla danego pracownika
            work_summary = WorkSummary.query.filter_by(employee_id=employee_id).first()
            if not work_summary:
                return jsonify({"error": "WorkStation not found"}), 404
            
            return jsonify({
                "employee_id": work_summary.employee_id,
                'date': work_summary.date,
                'task_id': work_summary.task_id,
                "work_time": float(work_summary.work_time) if work_summary.work_time is not None else None,
                "break_time": float(work_summary.break_time) if work_summary.break_time is not None else None
            }), 200
        except Exception as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
    elif request.method == 'POST':
        try:
            # Pobierz dane z żądania
            data = request.get_json()
            work_time = data.get('work_time')
            break_time = data.get('break_time')
            task_id = data.get('task_id')
            # Utwórz nowy rekord
            work_station = WorkSummary(
                employee_id=employee_id,
                # Czas pracy pracownika nad danym zadaniem w ciągu jednego dnia 
                work_time=work_time,
                # Czas przerwy pracownika w ciągu jednego dnia
                break_time=break_time,
                # ID zadania
                task_id=task_id,
                date=date.today(),
            )
            db.session.add(work_station)
            db.session.commit()
            return jsonify({"message": "WorkStation data saved successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 400


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

@app.route('/employee/<int:employee_id>/project/<int:project_id>/task_assignments', methods=['GET'])
def get_employee_project_task_assignment(employee_id, project_id):
    # Pobranie pracownika z bazy danych
    tasks = db.session.query(TaskAssignment).join(Task).join(Employee).filter(
        Employee.employee_id == employee_id, 
        Task.project_id == project_id
    ).all()
    task_assignments = []
    for task in tasks:
        task_assignments.append({
            'assignment_id': task.assignment_id,
            'assignment_name': task.name,
            'description': task.description,
            'start_date': task.start_date,
        })

    return jsonify(task_assignments)

# Dodano nową funkcje, wsysyła dane od nośnie zadań przypisanuych do konkretnego pracwnika 
@app.route('/employee/<int:employee_id>/task/<int:task_id>/assigned_tasks', methods=['GET'])
def get_employee_task_assignments(employee_id, task_id):
    tasks = []
    employee = Employee.query.get_or_404(employee_id)
    if employee:
        employee_task_assignments = employee.task_assignments
        if employee_task_assignments:
            for assignment in employee_task_assignments:
                task = Task.query.filter_by(task_id=task_id).first()
                if assignment.task_id == task_id:
                    tasks.append({
                        'assignment_id': assignment.assignment_id,
                        'task_name' : task.name,
                        'task_id': assignment.task_id,
                        'employee_id': assignment.employee_id,
                        'name': assignment.name,
                        'description': assignment.description,
                        'start_date': assignment.start_date,
                    })
    return jsonify(tasks)

# zmiana z /tasks -> /taskassignments
@app.route('/employee/<int:employee_id>/task_assignments', methods=['GET'])
def get_employee_tasks_assignments(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    tasks = []
    for task in employee.task_assignments:
        project_task = Task.query.get_or_404(task.task_id)
        project_name = Project.query.get_or_404(project_task.project_id)
        tasks.append({
            'assignment_id': task.assignment_id,
            'project_name': project_name.title,
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
            'name': task.name,
            'description': task.description,
            'start_date': task.start_date,
        })
    return jsonify(tasks)


@app.route('/project/task/<int:task_id>/assignments', methods=['GET'])
def get_project_task_assignments(task_id):
    task = Task.query.get_or_404(task_id)
    if task:
        task_assigments = []
        # project_tasks = project.tasks.query.filter_by(task_id=task_id).first()
        for task_assignment in task.assignments:
            if task_assignment:
                task_assigments.append({
                    'task_name' : task.name,
                    'assignment_id': task_assignment.assignment_id,
                    'employee_id': task_assignment.employee_id,
                    'assignment_name': task_assignment.name,
                    'description': task_assignment.description,
                    'start_date': task_assignment.start_date,
                })
    return jsonify(task_assigments)

# ************************************************************************************************************

# INICJALIZACJA BAZY DANYCH
with app.app_context():
    db.drop_all() 
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