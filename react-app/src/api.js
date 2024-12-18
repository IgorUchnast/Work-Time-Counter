import axios from "axios"

const API_URL = "http://localhost:5000"

export const getEmployees = () =>
    axios.get(`${API_URL}/employees`)

export const getEmployeeProjects = (employee_id) => 
    axios.get(`${API_URL}/employee/${employee_id}/projects`)

export const getEmployeeTasks = (employee_id) =>
    axios.get(`${API_URL}/employee/${employee_id}/tasks`)

export const getProjects = () =>
    axios.get(`${API_URL}/projects`)

export const getProjectTasks = (project_id) =>
    axios.get(`${API_URL}/project/${project_id}/tasks`)