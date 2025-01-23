import { useEffect, useState } from "react"
import { getProjectTasks, getTaskAssignments } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"

const ProjectTasksTab = ({ project_id }) => {
    const [tasks, setTasks] = useState([])
    const [expandedTaskId, setExpandedTaskId] = useState(null)

    const toggleTaskDetails = (taskId) => {
        setExpandedTaskId((prevTaskId) => (prevTaskId === taskId ? null : taskId))
    }

    useEffect(() => {
        getProjectTasks(project_id)
            .then((response) => {
                setTasks(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching project tasks:", err)
                setTasks([])
            })
    }, [project_id])

    if(!tasks.length) return <div>Brak zadań</div>

    return (
        <div>
            <h3>Zadania projektu {project_id}</h3>
            <ListGroup>
                {tasks.map((task) => (
                    <div key={task.task_id}>
                        <ListGroup.Item
                            onClick={() => toggleTaskDetails(task.task_id)}
                            style={{
                                cursor: "pointer",
                                backgroundColor: expandedTaskId === task.task_id ? "#f8f9fa" : "white",
                                border: "1px solid #ddd"
                            }}
                        >
                            <strong>{task.name}</strong>
                        </ListGroup.Item>
                        {expandedTaskId === task.task_id && (
                            <div style={{ marginBottom: "10px", padding: "10px", backgroundColor: "#f8f9fa", border: "1px solid #ddd" }}>
                                <ProjectTaskAssignments task_id={task.task_id} />
                            </div>
                        )}
                    </div>
                ))}
            </ListGroup>
        </div>
    )
}

const ProjectTaskAssignments = ({ task_id }) => {
    const [taskAssignments, setTaskAssignments] = useState([])

    useEffect(() => {
        getTaskAssignments(task_id)
            .then((response) => {
                setTaskAssignments(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching task assignments:", err)
                setTaskAssignments([])
            })
    }, [task_id])

    if(!taskAssignments.length) return <div>Brak podzadań</div>

    return (
        <div>
            <ListGroup>
                {taskAssignments.map((assignment) => (
                    <div key={assignment.assignment_id}>
                        <ListGroup.Item>
                            <p><strong>{assignment.assignment_name}</strong></p>
                            <p><strong>Opis: </strong>{assignment.description}</p>
                            <p><strong>Data rozpoczęcia: </strong>{assignment.start_date}</p>
                            <p><strong>Przypisane dla pracownika: </strong>{assignment.employee_id}</p>
                        </ListGroup.Item>
                    </div>
                ))}
            </ListGroup>
        </div>
    )
}

export default ProjectTasksTab