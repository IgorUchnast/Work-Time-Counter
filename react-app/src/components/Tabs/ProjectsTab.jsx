import { useEffect, useState } from "react"
import { getEmployeeProjects } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"
import { Link } from "react-router-dom";

const ProjectsTab = ({ employee_id }) => {
    const [projects, setProjects] = useState([])

    useEffect(() => {
        getEmployeeProjects(employee_id)
            .then((response) => {
                setProjects(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching employee projects:", err)
                setProjects([])
            })
    }, [employee_id])

    if(!projects.length) return <div>Ładowanie projektów pracownika...</div>

    return (
        <div>
            <h3>Projekty pracownika {employee_id}</h3>
            <ListGroup numbered>
                {projects.map((project) => (
                    <ListGroup.Item key={project.project_id}>
                        <Link to={`/project/${project.project_id}`} style={{ textDecoration: "none"}}>
                            {project.title}
                        </Link>
                    </ListGroup.Item>
                ))}
            </ListGroup>
        </div>
    )
}

export default ProjectsTab