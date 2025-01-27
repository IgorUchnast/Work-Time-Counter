import { useEffect, useState } from "react"
import { getEmployeeTasks } from "../../api"
import ListGroup from "react-bootstrap/ListGroup"

const EmployeeTasksTab = ({ employee_id }) => {
    const [tasks, setTasks] = useState([])
    const [expandedTaskId, setExpandedTaskId] = useState(null)

    const toggleTaskDetails = (taskId) => {
        setExpandedTaskId((prevTaskId) => (prevTaskId === taskId ? null : taskId))
    }

    useEffect(() => {
        getEmployeeTasks(employee_id)
            .then((response) => {
                setTasks(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching employee tasks:", err)
                setTasks([])
            })
    }, [employee_id])

    if(!tasks.length) return <div>Brak zadań</div>

    return (
        <div>
            <h3>Zadania pracownika {employee_id}</h3>
            <ListGroup>
                {tasks.map((task) => (
                    <div key={task.assignment_id}>
                        <ListGroup.Item
                            onClick={() => toggleTaskDetails(task.assignment_id)}
                            style={{
                                cursor: "pointer",
                                backgroundColor: expandedTaskId === task.assignment_id ? "#f8f9fa" : "white",
                                border: "1px solid #ddd"
                            }}
                        >
                            <strong>{task.name}</strong> <i>({task.status})</i>
                        </ListGroup.Item>
                        {expandedTaskId === task.assignment_id && (
                            <div style={{ marginBottom: "10px", padding: "10px", backgroundColor: "#f8f9fa", border: "1px solid #ddd" }}>
                                <strong>Id zadania: </strong>{task.task_id}<br/>
                                <strong>Opis: </strong>{task.description}<br/>
                                <strong>Data ostatniego rozpoczęcia: </strong>{task.start_date ? (task.start_date) : ("brak")}<br/>
                                <strong>Data ostatniego zakończenia: </strong>{task.stop_date ? (task.stop_date) : ("brak")}
                            </div>
                        )}
                    </div>
                ))}
            </ListGroup>
        </div>
    )
}

export default EmployeeTasksTab