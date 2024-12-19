import { useEffect, useState } from "react"
import { getProjectTasks } from "../../api"
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

    if(!tasks.length) return <div>Ładowanie zadań...</div>

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
                                <p><strong>Opis: </strong>{task.description}</p>
                                <p><strong>Data rozpoczęcia: </strong>{task.start_date}</p>
                            </div>
                        )}
                    </div>
                ))}
            </ListGroup>
        </div>
    )
}

export default ProjectTasksTab