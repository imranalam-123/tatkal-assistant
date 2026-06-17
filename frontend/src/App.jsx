import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import SearchTrain from "./pages/SearchTrain";
import MyBookings from "./pages/MyBookings";
import PNRStatus from "./pages/PNRStatus";
import PassengerDetails from "./pages/PassengerDetails";
import Tickets from "./pages/Tickets";
import Payment from "./pages/Payment";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/search-train"
          element={<SearchTrain />}
        />

        <Route
          path="/my-bookings"
          element={<MyBookings />}
        />

        <Route
          path="/pnr-status"
          element={<PNRStatus />}
        />

        <Route
          path="/passenger-details"
          element={<PassengerDetails />}
        />

        <Route
          path="/tickets"
          element={<Tickets />}
        />

        <Route
          path="/payment"
          element={<Payment />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;