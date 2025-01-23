import { useEffect, useState } from "react"
import { getEmployeeWorkData } from "../../api"
import { BarChart } from "@mui/x-charts"

const EmployeeSummaryTab = ({ employee_id }) => {
    const [workData, setWorkData] = useState(null)
    const [loading, setLoading] = useState(true)

    // curl -X POST "http://localhost:5000/employee/1/work_summary" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"work_time\": 6.5, \"break_time\": 1.5, \"task_id\": 1}"

    useEffect(() => {
        setLoading(true)
        getEmployeeWorkData(employee_id)
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
        let xAxisData = []
        let workTimeData = []
        let breakTimeData = []

        if (data === undefined || data === null) {
            console.log("Brak danych")
        } else if (typeof data === 'object') {
            xAxisData.push(new Date(data.date).toISOString().split("T")[0])
            workTimeData.push(data.work_time)
            breakTimeData.push(data.break_time)
        } else if (Array.isArray(data)) {
            xAxisData = data.map((item) => {
                if(!item.date) {
                    console.error("Invalid date value:", item.date);
                    return "Invalid Date"; // Domyślna wartość dla błędnych dat
                }
                const parsedDate = new Date(item.date)
                if(isNaN(parsedDate)) {
                    console.error("Unable to parse date:", item.date);
                    return "Invalid Date"; // Domyślna wartość dla błędnych dat
                }
                return parsedDate.toISOString.split("T")[0]
            })
            workTimeData = data.map((item) => item.work_time || 0);
            breakTimeData = data.map((item) => item.break_time || 0);
        }
        
        return {
            xAxisData,
            series: [
                { label: 'Godziny pracy', data: workTimeData },
                { label: 'Godziny przerwy', data: breakTimeData },
            ],
        };
    };

    if(loading) return <div>Ładowanie danych...</div>

    const { xAxisData, series } = processDataForChart(workData);

    return (
        <div>
            <h3>Podsumowanie czasu pracy pracownika {employee_id}</h3>
            <BarChart
                xAxis={[{ scaleType: "band", data: xAxisData}]}
                series={series}
                width={500}
                height={300}
            />
        </div>
    )
}

export default EmployeeSummaryTab