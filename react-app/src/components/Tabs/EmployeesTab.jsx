import React, { useEffect, useState } from "react"
import { getProjectMembers } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"
import { Link } from "react-router-dom"
import { EmployeeProjectTaskAssignments } from "./ProjectsTab"

const EmployeesTab = ({ project_id }) => {
    const [employees, setEmployees] = useState([])
    const [expandedEmployeeId, setExpandedEmployeeId] = useState(null)

    const toggleEmployeeTasks = (employeeId) => {
        setExpandedEmployeeId((prevEmployeeId) => (prevEmployeeId === employeeId ? null : employeeId))
    }

    useEffect(() => {
        getProjectMembers(project_id)
            .then((response) => {
                setEmployees(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching project members:", err)
                setEmployees([])
            })
    }, [project_id])

    if(!employees.length) return <div>Brak pracowników projektu</div>

    return (
        <div>
            <h3>Pracownicy projektu {project_id}</h3>
            <ListGroup numbered>
                {employees.map((employee) => (
                    <React.Fragment key={employee.employee_id}>
                        <ListGroup.Item
                            onClick={() => toggleEmployeeTasks(employee.employee_id)}
                            style={{
                                cursor: "pointer",
                                backgroundColor: expandedEmployeeId === employee.employee_id ? "#f8f9fa" : "white",
                                border: "1px solid #ddd"
                            }}
                        >
                            <Link to={`/employee/${employee.employee_id}`} style={{ textDecoration: "none" }}>
                                {employee.first_name} {employee.last_name}
                            </Link>
                        </ListGroup.Item>
                        {expandedEmployeeId === employee.employee_id && (
                            <div
                                style={{
                                    marginBottom: "10px", 
                                    padding: "10px", 
                                    backgroundColor: "#f8f9fa", 
                                    border: "1px solid #ddd"
                                }}
                            >
                                <EmployeeProjectTaskAssignments
                                    employee_id={employee.employee_id}
                                    project_id={project_id}
                                />
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </ListGroup>
        </div>
    )
}

export default EmployeesTab