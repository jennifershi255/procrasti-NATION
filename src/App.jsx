import {Route, Routes} from 'react-router-dom'
import Home from './pages/Home';
import './App.css'
import Excuse from './pages/Excuse';
import HistoryPage from './pages/History';
import LockIn from './pages/Lock-In';

const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/excuse" element={<Excuse />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/lock-in" element = {<LockIn />}/>
      </Routes>
    </div>
  )
};

export default App;