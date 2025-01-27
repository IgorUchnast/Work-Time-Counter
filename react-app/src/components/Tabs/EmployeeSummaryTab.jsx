import { useEffect, useState } from "react"
import { getEmployeeWorkTimeSummary } from "../../api"
import { BarChart } from "@mui/x-charts"

const EmployeeSummaryTab = ({ employee_id }) => {
    const [workData, setWorkData] = useState(null)
    const [loading, setLoading] = useState(true)

    // curl -X POST "http://localhost:5000/employee/1/work_summary" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"work_time\": 6.5, \"break_time\": 1.5, \"task_id\": 1}"

    useEffect(() => {
        setLoading(true)
        getEmployeeWorkTimeSummary(employee_id)
            .then((response) => {
                setWorkData(response.data || null)
            })
            .catch((err) => {
                console.error("Error fetching work data:", err)
                setWorkData(null)
            })
            .finally(() => setLoading(false))
    }, [employee_id])

    // Funkcja mapująca dane na format wykresu
    const processDataForChart = (data) => {
        // Handle null, undefined, or non-array JSON
        if (!data || !Array.isArray(data) || data.length === 0) {
            return { 
                xAxisData: [], 
                series: [{ label: 'Brak danych', data: [] }]
            }
        }

        // Extract dates for x-axis
        const xAxisData = data.map(item => item.date || 'Nieznana data').reverse();

        // Prepare series for break time and each unique task
        const taskIds = [...new Set(
            data.flatMap(day => 
                (day.task_time || []).map(task => task.task_id)
            )
        )]
        
        const series = [
            // Break time series
            {
                label: 'Przerwy',
                data: data.map(item => item.break_time || 0).reverse()
            },
            // Series for each task
            ...taskIds.map(taskId => ({
                label: `Zadanie ${taskId}`,
                data: data.map(day => {
                    const taskEntry = (day.task_time || [])
                        .find(task => task.task_id === taskId);
                    return taskEntry ? (taskEntry.work_time || 0) : 0;
                }).reverse()
            }))
        ];

        return { xAxisData, series };
    };

    // Funkcja mapująca dane na sumujący wykres
    const processWorkTotalChart = (data) => {
        // If no data, return default series
        if (!data || !Array.isArray(data) || data.length === 0) {
            return { 
                xAxisData: [], 
                series: []
            };
        }
    
        const xAxisData = data.map(item => item.date || 'Nieznana data').reverse();
    
        const series = [
            {
                label: 'Czas przerwy',
                data: data.map(item => item.break_time || 0).reverse()
            },
            {
                label: 'Całkowity czas pracy',
                data: data.map(item => item.sum_work_time || 0).reverse()
            }
        ];
    
        return { xAxisData, series };
    };

    if(loading) return <div>Ładowanie danych...</div>

    const { xAxisData, series } = processDataForChart(workData);
    const { xAxisData: xAxisDataTotal, series: seriesTotal } = processWorkTotalChart(workData);

    return (
        <div>
            <h3>Podsumowanie czasu pracy pracownika {employee_id} w danych dniach</h3>
            <h5>Łączny czas pracy w trakcie dnia</h5>
            <div>
                <BarChart
                    xAxis={[{ scaleType: "band", data: xAxisDataTotal}]}
                    series={seriesTotal}
                    width={1000}
                    height={300}
                />
            </div>
            <h5>Rozłożony czas pracy nad poszczególnymi zadaniami</h5>
            <div>
                <BarChart
                    xAxis={[{ scaleType: "band", data: xAxisData}]}
                    series={series}
                    width={1000}
                    height={300}
                />
            </div>
        </div>
    )
}

export default EmployeeSummaryTab