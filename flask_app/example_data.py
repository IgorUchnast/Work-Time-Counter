from datetime import datetime, timedelta
from random import randint, uniform
from models.models import Employee, TaskAssignment, WorkSummary
from db.db_configuration import db

def add_sample_work_summary():
    # Pobierz wszystkie dostępne przypisania zadań
    task_assignments = TaskAssignment.query.all()
    
    if not task_assignments:
        print("No task assignments found in the database.")
        return

    for day_offset in range(10):  # Dla 5 dni
        date = datetime.utcnow().date() - timedelta(days=day_offset)

        for task_assignment in task_assignments:
            if task_assignment.employee_id is not None:  # Dodaj tylko jeśli jest przypisany pracownik
                for _ in range(2):  # 3 wpisy na dzień
                    work_time = round(uniform(300, 1800), 2)  # Losowe wartości czasu pracy (1-3 godziny)
                    break_time = round(uniform(300,600), 2)  # Losowe wartości przerw (6-30 minut)

                    work_summary = WorkSummary(
                        employee_id=task_assignment.employee_id,
                        task_id=task_assignment.task_id,
                        work_time=work_time/3600,
                        break_time=break_time/3600,
                        date=date
                    )
                    db.session.add(work_summary)
    db.session.commit()
    print("Sample work summaries added successfully.")

