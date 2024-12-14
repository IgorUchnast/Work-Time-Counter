from config.api_key import WORK_SPACE
from trello_data.get_trello_data import get_boards_in_workspace, get_trello_data, get_trello_member_cards, get_trello_cards
from models.models import Employee, Project, Task, TaskAssignment
from trello_data.save_trello_data_to_db import save_trello_employee, save_trello_lists, save_trello_cards
from db.db_configuration import db
from datetime import date
from datetime import datetime

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
                    leader_id = 0
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
                for listt in lists:
                    save_trello_lists(board_id=board_id)
                    save_trello_cards(list_id=listt['id'])


def fetch_trello_employee():
    boards = get_boards_in_workspace(WORK_SPACE)
    if boards:
        for board in boards:
            board_id = board['id']
            members = get_trello_data(board_id=board_id, data_type='members')
            if members:
                for member in members:
                    save_trello_employee(board_id=board_id)
            memberships = get_trello_data(board_id, data_type='memberships')
            if memberships:
                for member in memberships:
                    if member["memberType"] == "admin":
                        employees = Employee.query.all()
                        for employee in employees:
                            if employee.email.split('_')[-1].split('@')[0] == member["idMember"]:
                                project = Project.query.filter_by(description=board_id).first()
                                project.leader_id = employee.employee_id
                                db.session.commit()

