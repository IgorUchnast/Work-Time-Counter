import { useEffect, useState } from "react";
import { getTaskAssignments } from "../../api";
import ListGroup from "react-bootstrap/ListGroup"

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

    if(!taskAssignments.length) return <div>Ładowanie podzadań...</div>

    return (
        <div>
            <ListGroup>
                {taskAssignments.map((assignment) => (
                    <div 
                        key={assignment.assignment_id}
                        // style={{ marginBottom: "10px", padding: "10px", backgroundColor: "#f8f9fa", border: "1px solid #ddd" }}
                    >
                        <ListGroup.Item>
                            <p><strong>{assignment.name}</strong></p>
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

export default ProjectTaskAssignments