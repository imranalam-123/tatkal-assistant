import { useEffect, useState } from "react";
import api from "../services/api";

function MyBookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get(
        "/booking/all",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setBookings(response.data);

    } catch (error) {
      console.log(
        "FETCH BOOKINGS ERROR:",
        error
      );
    }
  };

  const cancelBooking = async (
    bookingId
  ) => {
    try {
      const token =
        localStorage.getItem("token");

      const response = await api.delete(
        `/booking/cancel/${bookingId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "CANCEL RESPONSE:",
        response.data
      );

      alert(
        "Booking Cancelled Successfully"
      );

      fetchBookings();

    } catch (error) {
      console.log(
        "CANCEL ERROR:",
        error.response?.data
      );

      alert(
        error.response?.data?.detail ||
          "Cancellation Failed"
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
      <h1>My Bookings</h1>

      {bookings.length === 0 ? (
        <h3>No Bookings Found</h3>
      ) : (
        bookings.map((booking) => (
          <div
            key={booking.id}
            style={{
              border: "1px solid gray",
              margin: "10px auto",
              padding: "10px",
              width: "500px",
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

            <button
              onClick={() =>
                cancelBooking(
                  booking.id
                )
              }
              disabled={
                booking.status ===
                "CANCELLED"
              }
              style={{
                padding:
                  "8px 15px",
                cursor: "pointer",
              }}
            >
              {booking.status ===
              "CANCELLED"
                ? "Cancelled"
                : "Cancel Booking"}
            </button>
          </div>
        ))
      )}
    </div>
  );
}

export default MyBookings;