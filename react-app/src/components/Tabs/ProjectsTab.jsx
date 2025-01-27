import React, { useEffect, useState } from "react"
import { getEmployeeProjects, getEmployeeProjectTaskAssignments } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"
import { Link } from "react-router-dom";

const ProjectsTab = ({ employee_id }) => {
    const [projects, setProjects] = useState([])
    const [expandedProjectId, setExpandedProjectId] = useState(null)

    const toggleProjectTasks = (projectId) => {
        setExpandedProjectId((prevProjectId) => (prevProjectId === projectId ? null : projectId))
    }

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

    if(!projects.length) return <div>Brak projektów pracownika</div>

    return (
        <div>
            <h3>Projekty pracownika {employee_id}</h3>
            <ListGroup numbered>
                {projects.map((project) => (
                    <React.Fragment key={project.project_id}>
                        <ListGroup.Item
                            onClick={() => toggleProjectTasks(project.project_id)}
                            style={{
                                cursor: "pointer",
                                backgroundColor: expandedProjectId === project.project_id ? "#f8f9fa" : "white",
                                border: "1px solid #ddd"
                            }}
                        >
                            <Link 
                                to={`/project/${project.project_id}`} 
                                style={{ textDecoration: "none"}}
                            >
                                {project.title}
                            </Link>
                        </ListGroup.Item>
                        {expandedProjectId === project.project_id && (
                            <div 
                                style={{ 
                                    marginBottom: "10px", 
                                    padding: "10px", 
                                    backgroundColor: "#f8f9fa", 
                                    border: "1px solid #ddd" 
                                }}
                            >
                                <EmployeeProjectTaskAssignments
                                    employee_id={employee_id}
                                    project_id={project.project_id}
                                />
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </ListGroup>
        </div>
    )
}

export const EmployeeProjectTaskAssignments = ({ employee_id, project_id }) => {
    const [projectTaskAssignments, setProjectTaskAssignments] = useState([])
    

    useEffect(() => {
        getEmployeeProjectTaskAssignments(employee_id, project_id)
            .then((response) => {
                setProjectTaskAssignments(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching employee tasks:", err)
                setProjectTaskAssignments([])
            })
    }, [employee_id, project_id])

    if(!projectTaskAssignments.length) return <div>Brak podzadań</div>

    return (
        <div>
            <ListGroup>
                {projectTaskAssignments.map((assignment) => (
                    <div key={assignment.assignment_id}>
                        <ListGroup.Item>
                            <strong>{assignment.assignment_name}</strong> <i>({assignment.status})</i><br/>
                            <strong>Id zadania: </strong>{assignment.assignment_id}<br/>
                            <strong>Opis: </strong>{assignment.description}<br/>
                            <strong>Data ostatniego rozpoczęcia: </strong>{assignment.start_date ? (assignment.start_date) : ("brak")}<br/>
                            <strong>Data ostatniego zakończenia: </strong>{assignment.stop_date ? (assignment.stop_date) : ("brak")}
                        </ListGroup.Item>
                    </div>
                ))}
            </ListGroup>
        </div>
    )
}

export default ProjectsTab