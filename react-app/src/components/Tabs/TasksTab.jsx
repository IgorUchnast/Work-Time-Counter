import { useEffect, useState } from "react"
import { getEmployeeTasks, getProjectTasks } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"

const TasksTab = ({ employee_id, project_id }) => {
    const [tasks, setTasks] = useState([])
    const [expandedTaskId, setExpandedTaskId] = useState(null)

    const toggleTaskDetails = (taskId) => {
        setExpandedTaskId((prevTaskId) => (prevTaskId === taskId ? null : taskId))
    }

    useEffect(() => {
        if(employee_id) {
            getEmployeeTasks(employee_id)
                .then((response) => {
                    setTasks(response.data || [])
                })
                .catch((err) => {
                    console.error("Error fetching employee tasks:", err)
                    setTasks([])
                })
        }
        if(project_id) {
            getProjectTasks(project_id)
                .then((response) => {
                    setTasks(response.data || [])
                })
                .catch((err) => {
                    console.error("Error fetching project tasks:", err)
                    setTasks([])
                })
        }
    }, [ employee_id, project_id])

    if(!tasks.length) return <div>Ładowanie zadań...</div>

    return (
        <div>
            {project_id === null && (
                <h3>Zadania pracownika {employee_id}</h3>
            )}
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
                                <p><strong>Id projektu: </strong>{task.project_id}</p>
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

export default TasksTab