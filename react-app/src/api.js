import axios from "axios"

const API_URL = "http://127.0.0.1:5000"

export const getEmployees = () =>
    axios.get(`${API_URL}/employees`)

export const getEmployeeProjects = (employee_id) =>
    axios.get(`${API_URL}/employee/${employee_id}/projects`)

export const getEmployeeTasks = (employee_id) =>
    axios.get(`${API_URL}/employee/${employee_id}/task_assignments`)

export const getProjects = () =>
    axios.get(`${API_URL}/projects`)

export const getProjectMembers = (project_id) =>
    axios.get(`${API_URL}/project/${project_id}/members`)

export const getProjectTasks = (project_id) =>
    axios.get(`${API_URL}/project/${project_id}/tasks`)