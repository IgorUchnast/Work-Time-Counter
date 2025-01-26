import { useEffect, useState } from "react"
import { getProjectWorkTimeSummary } from "../../api"
import { pieArcLabelClasses, PieChart } from "@mui/x-charts"

const ProjectSummaryTab = ({ project_id }) => {
    const [workData, setWorkData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        setLoading(true)
        getProjectWorkTimeSummary(project_id)
            .then((response) => {
                setWorkData(response.data || null)
            })
            .catch((err) => {
                console.error("Error fetching work data:", err)
                setWorkData(null)
            })
            .finally(() => setLoading(false))
    }, [project_id])

    // Funkcja mapująca dane na wykres kołowy
    const processDataForPieChart = (data) => {
        // If no data, return default series
        if (!data || !Array.isArray(data) || data.length === 0) {
            return { 
                innerData: [],
                outerData: []
            };
        }

        const innerData = data
            .filter(task => task.task_assignments && task.task_assignments.length > 0)
            .map(task => ({
                label: task.task_name || 'Nieznane zadanie',
                value: task.task_work_time || 0
            }));

        const outerData = data.flatMap(task => 
            (task.task_assignments || []).map(assignment => ({
                label: `${task.task_name || 'Nieznane zadanie'}: ${assignment.task_assignment || 'Nieznane podzadanie'}`,
                value: assignment.work_time || 0
            }))
        );
    
        return { innerData, outerData };
    };

    if(loading) return <div>Ładowanie danych...</div>

    const { innerData, outerData } = processDataForPieChart(workData);
    const innerTotal = innerData.map((item) => item.value).reduce((a, b) => a + b, 0)
    const outerTotal = outerData.map((item) => item.value).reduce((a, b) => a + b, 0)
    const getInnerArcLabel = (params) => {
        const percent = params.value / innerTotal
        return `${(percent * 100).toFixed(0)}%`
    }
    const getOuterArcLabel = (params) => {
        const percent = params.value / outerTotal
        return `${(percent * 100).toFixed(0)}%`
    }

    return (
        <div>
            <h3>Podsumowanie sumy czasu pracy nad projektem {project_id}</h3>
            <h5>Łączny czas pracy nad zadaniami i podzadaniami projektu</h5>
            <div>
                <PieChart
                    series={[
                        {
                            innerRadius: 0,
                            outerRadius: '50%',
                            data: innerData,
                            arcLabel: getInnerArcLabel,
                            cx: '30%'
                        },
                        {
                            innerRadius: '60%',
                            outerRadius: '80%',
                            data: outerData,
                            arcLabel: getOuterArcLabel,
                            cx: '30%'
                        },
                    ]}
                    sx={{
                        [`& .${pieArcLabelClasses.root}`]: {
                            fill: 'white',
                            fontSize: 14,
                        },
                    }}
                    width={1000}
                    height={500}
                    margin={{
                        right: 0
                    }}
                    slotProps={{
                        legend: {
                            direction: 'column',
                            position: { vertical: 'middle', horizontal: 'right' },
                            padding: 0,
                        },
                    }}
                />
            </div>
        </div>
    )
}

export default ProjectSummaryTab