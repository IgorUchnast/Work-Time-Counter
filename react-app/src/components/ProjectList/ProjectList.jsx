import { useEffect, useState } from "react"
import { getProjects } from "../../api"
import ProjectItem from "./ProjectItem"

const ProjectList = () => {
    const [projects, setProjects] = useState([])
    const [error, setError] = useState(null)

    // Pierwszy render
    useEffect(() => {
        getProjects()
            .then((response) => setProjects(response.data))
            .catch((err) => {
                console.error("Error fetching project list:", err)
                setError("Nie udało się pobrać listy projektów")
            })
    }, [])

    if(error) return <div className="error">{error}</div>

    // Jeśli dane nie zostały jeszcze załadaowane
    if(!projects.length) return <div>Ładowanie projektów...</div>

    return (
        <div className="project-list">
            <h3>Lista projektów:</h3>
            <ul>
                {projects.map((project) => (
                    <ProjectItem 
                        key={project.project_id}
                        title={project.title}
                        description={project.description}
                        start_date={project.start_date}
                        leader_id={project.leader_id}
                    />
                ))}
            </ul>
        </div>
    )
}

export default ProjectList