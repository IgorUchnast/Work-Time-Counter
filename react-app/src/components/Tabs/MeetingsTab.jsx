const MeetingsTab = ({ employee_id, project_id }) => {
    return (
        <div>
            <h3>Spotkania</h3>
            <p>Lista spotkań pracownika {employee_id}/projektu {project_id}</p>
        </div>
    )
}

export default MeetingsTab