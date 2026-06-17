import { useState } from "react";
import api from "../services/api";

function PNRStatus() {
  const [pnr, setPnr] = useState("");
  const [booking, setBooking] = useState(null);

  const checkPNR = async () => {
    try {
      const token =
        localStorage.getItem("token");

      const response = await api.get(
        `/pnr/${pnr}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "PNR RESPONSE:",
        response.data
      );

      setBooking(response.data);

    } catch (error) {
      console.log(
        "PNR ERROR:",
        error.response?.data
      );

      alert(
        error.response?.data?.detail ||
          "PNR Not Found"
      );
    }
  };

  return (
    <div
      style={{
        color: "white",
        textAlign: "center",
        marginTop: "50px",
      }}
    >
      <h1>PNR Status</h1>

      <input
        type="text"
        placeholder="Enter PNR Number"
        value={pnr}
        onChange={(e) =>
          setPnr(e.target.value)
        }
      />

      <br />
      <br />

      <button onClick={checkPNR}>
        Check Status
      </button>

      <br />
      <br />

      {booking && (
        <div
          style={{
            border: "1px solid gray",
            width: "500px",
            margin: "auto",
            padding: "15px",
          }}
        >
          <p>
            <strong>PNR:</strong>{" "}
            {booking.pnr}
          </p>

          <p>
            <strong>Train No:</strong>{" "}
            {booking.train_no}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            {booking.status}
          </p>

          <p>
            <strong>Coach:</strong>{" "}
            {booking.coach || "-"}
          </p>

          <p>
            <strong>Seat No:</strong>{" "}
            {booking.seat_no || "-"}
          </p>

          <p>
            <strong>Berth:</strong>{" "}
            {booking.berth || "-"}
          </p>
        </div>
      )}
    </div>
  );
}

export default PNRStatus;