import Tab from 'react-bootstrap/Tab'
import Tabs from 'react-bootstrap/Tabs'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import ProjectsTab from './Tabs/ProjectsTab'
import EmployeesTab from './Tabs/EmployeesTab'
import { useParams } from 'react-router-dom'
import Sidebar from './Sidebar/Sidebar'
import EmployeeTasksTab from './Tabs/EmployeeTasksTab'
import ProjectTasksTab from './Tabs/ProjectTasksTab'
import EmployeeSummaryTab from './Tabs/EmployeeSummaryTab'
import ProjectSummaryTab from './Tabs/ProjectSummaryTab'

const Dashboard = ({ type }) => {
    let params = useParams()

    return (
        <Container fluid>
            <Row>
                {/* Sidebar zajmujący 3 z 12 kolumn */}
                <Col md={2} className='p-0'>
                    <Sidebar />
                </Col>
                
                {/* Główna sekcja Tabs */}
                <Col md={10}>
                    {type !== null && (type === "employees" ? (
                        <Tabs
                            id={type}
                            defaultActiveKey="summary"
                            variant='underline'
                            className="mb-3"
                            justify
                        >
                            <Tab eventKey="summary" title="Podsumowanie">
                                <EmployeeSummaryTab employee_id={params.employee_id}/>
                            </Tab>
                            <Tab eventKey="projects" title="Projekty">
                                <ProjectsTab employee_id={params.employee_id}/>
                            </Tab>
                            <Tab eventKey="tasks" title="Zadania">
                                <EmployeeTasksTab employee_id={params.employee_id}/>
                            </Tab>
                        </Tabs>
                        ) : (
                        <Tabs
                            id={type}
                            defaultActiveKey="summary"
                            variant='underline'
                            className="mb-3"
                            justify
                        >
                            <Tab eventKey="summary" title="Podsumowanie">
                                <ProjectSummaryTab project_id={params.project_id}/>
                            </Tab>
                            <Tab eventKey="employees" title="Pracownicy">
                                <EmployeesTab project_id={params.project_id}/>
                            </Tab>
                            <Tab eventKey="tasks" title="Zadania">
                                <ProjectTasksTab project_id={params.project_id}/>
                            </Tab>
                        </Tabs>
                    ))}
                </Col>
            </Row>
        </Container>
    )
}

export default Dashboard