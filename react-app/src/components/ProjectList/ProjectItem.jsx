const ProjectItem = ({ title, description, start_date, leader_id }) => {
    return (
        <li className="project-item">
            <h4>{title}</h4>
            <p>{description}</p>
        </li>
    )
}

export default ProjectItem