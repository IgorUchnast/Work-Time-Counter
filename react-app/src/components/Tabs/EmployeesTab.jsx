import { useEffect, useState } from "react"
import { getProjectMembers } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"
import { Link } from "react-router-dom"

const EmployeesTab = ({ project_id }) => {
    const [employees, setEmployees] = useState([])

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

    if(!employees.length) return <div>Ładowanie pracowników projektu...</div>

    return (
        <div>
            <h3>Pracownicy projektu {project_id}</h3>
            <ListGroup numbered>
                {employees.map((employee) => (
                    <ListGroup.Item key={employee.employee_id}>
                        <Link to={`/employee/${employee.employee_id}`} style={{ textDecoration: "none" }}>
                            {employee.first_name} {employee.last_name}
                        </Link>
                    </ListGroup.Item>
                ))}
            </ListGroup>
        </div>
    )
}

export default EmployeesTab