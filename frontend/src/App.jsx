import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import SearchTrain from "./pages/SearchTrain";
import MyBookings from "./pages/MyBookings";
import PNRStatus from "./pages/PNRStatus";
import PassengerDetails from "./pages/PassengerDetails";
import Tickets from "./pages/Tickets";
import Payment from "./pages/Payment";

function Shell({ children }) {
  return (
    <div className="app-shell">
      <main className="page">
        <nav className="navbar" aria-label="Primary navigation">
          <Link className="logo" to="/dashboard">
            <span className="logo-mark">🚆</span>
            <span>Tatkal Assistant</span>
          </Link>
          <div className="nav-links">
            <Link to="/search-train">Search</Link>
            <Link to="/passenger-details">Passengers</Link>
            <Link to="/my-bookings">Bookings</Link>
            <Link to="/tickets">Tickets</Link>
            <Link to="/pnr-status">PNR</Link>
          </div>
        </nav>
        {children}
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Shell>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/search-train" element={<SearchTrain />} />
          <Route path="/my-bookings" element={<MyBookings />} />
          <Route path="/pnr-status" element={<PNRStatus />} />
          <Route path="/passenger-details" element={<PassengerDetails />} />
          <Route path="/tickets" element={<Tickets />} />
          <Route path="/payment" element={<Payment />} />
        </Routes>
      </Shell>
    </BrowserRouter>
  );
}

export default App;
