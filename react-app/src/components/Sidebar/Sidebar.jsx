import { useEffect, useState } from "react"
import { getEmployees, getProjects } from "../../api"
import Collapse from "react-bootstrap/esm/Collapse";
import Button from "react-bootstrap/esm/Button";
import ListGroup from "react-bootstrap/ListGroup"
import { Link } from "react-router-dom";

const Sidebar = () => {
    const [employees, setEmployees] = useState([])
    const [projects, setProjects] = useState([])

    // Stany kontrolujące rozwinięcie sekcji
    const [showEmployees, setShowEmployees] = useState(false);
    const [showProjects, setShowProjects] = useState(false);

    // Funkcje przełączające widoczność sekcji
    const toggleEmployees = () => setShowEmployees(!showEmployees);
    const toggleProjects = () => setShowProjects(!showProjects);

    useEffect(() => {
        getEmployees()
            .then((response) => {
                setEmployees(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching employees:", err)
                setEmployees([])
            })
        getProjects()
            .then((response) => {
                setProjects(response.data || [])
            })
            .catch((err) => {
                console.error("Error fetching data:", err)
                setProjects([])
            })
    }, [])

    if(!employees.length) return <div>Ładowanie pracowników...</div>
    if(!projects.length) return <div>Ładowanie projektów...</div>

    return (
        <div style={{ position: "sticky", top: "0", overflowY: "auto", height: "100vh", backgroundColor: "#f8f9fa", padding: "10px", borderRight: "1px solid #ddd" }}>
            <Link
                to='/'
                style={{
                    textDecoration: "none", // Usuwa podkreślenie
                    color: "inherit", // Dziedziczy kolor tekstu
                    cursor: "pointer" // Zmienia kursor na wskaźnik
                }}
            >
                <h4 className="mb-3">WorkTime Counter</h4>
            </Link>

            {/* Sekcja Pracownicy */}
            <Button
                variant="light"
                onClick={toggleEmployees}
                aria-controls="employees-list"
                aria-expanded={showEmployees}
                className="w-100 text-start"
            >
                {showEmployees ? "▼ Pracownicy" : "▶ Pracownicy"}
            </Button>
            <Collapse in={showEmployees}>
                <div id="employees-list">
                    <ListGroup numbered>
                        {employees.map((employee) => (
                            <ListGroup.Item key={employee.employee_id}>
                                <Link to={`/employee/${employee.employee_id}`} style={{ textDecoration: "none"}}>
                                    {employee.first_name} {employee.last_name}
                                </Link>
                            </ListGroup.Item> 
                        ))}
                    </ListGroup>
                </div>
            </Collapse>

            {/* Sekcja Projekty */}
            <Button
                variant="light"
                onClick={toggleProjects}
                aria-controls="projects-list"
                aria-expanded={showProjects}
                className="w-100 text-start mt-2"
            >
                {showProjects ? "▼ Projekty" : "▶ Projekty"}
            </Button>
            <Collapse in={showProjects}>
                <div id="projects-list">
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
            </Collapse>
        </div>
    )
}

export default Sidebar