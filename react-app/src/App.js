import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from './components/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Dashboard type={null}/>} />
        <Route path='/employee/:employee_id' element={<Dashboard type='employees'/>} />
        <Route path='/project/:project_id' element={<Dashboard type='projects'/>} />
        {/* <Route path='*' element={<NotFound />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
