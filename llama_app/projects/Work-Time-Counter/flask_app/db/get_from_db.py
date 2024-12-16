from flask import Flask, jsonify, request
from models.models import Employee, Project, ProjectMember, Task, TaskAssignment, WorkStation, Meeting, MeetingAttendance
from db_configuration import db, app

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


@app.route('/project_members/<int:project_id>', methods=['GET'])
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