import { useState, useEffect } from "react";
import api from "../services/api";

function SearchTrain() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [journeyDate, setJourneyDate] = useState("");

  const [trains, setTrains] = useState([]);
  const [passengers, setPassengers] = useState([]);
  const [selectedPassenger, setSelectedPassenger] =
    useState("");

  useEffect(() => {
    fetchPassengers();
  }, []);

  const fetchPassengers = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get(
        "/passenger/all",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "PASSENGERS:",
        response.data
      );

      setPassengers(response.data);

    } catch (error) {
      console.log(
        "PASSENGER ERROR:",
        error
      );
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    if (!token) {
      alert("Please Login First");
      return;
    }

    try {
      const response = await api.post(
        `/train/search?source=${source}&destination=${destination}&journey_date=${journeyDate}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "SEARCH RESPONSE:",
        response.data
      );

      setTrains(response.data.trains);

    } catch (error) {
      console.log(
        "SEARCH ERROR:",
        error.response?.data
      );

      alert("Train Search Failed");
    }
  };

  const bookTrain = async (train) => {
    if (!selectedPassenger) {
      alert(
        "Please Select Passenger First"
      );
      return;
    }

    if (!journeyDate) {
      alert(
        "Please Select Journey Date"
      );
      return;
    }

    try {
      const token = localStorage.getItem("token");

      const response = await api.post(
        "/booking/create",
        {
          passenger_id:
            Number(selectedPassenger),
          train_no: train.train_no,
          journey_date: journeyDate,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "BOOKING RESPONSE:",
        response.data
      );

      alert(
        `Booking Successful

PNR: ${response.data.pnr}

Status: ${response.data.status}

Coach: ${response.data.coach || "-"}

Seat No: ${response.data.seat_no || "-"}

Berth: ${response.data.berth || "-"}

RAC Number: ${
          response.data.rac_number || "-"
        }

Waiting List Number: ${
          response.data.wl_number || "-"
        }`
      );

    } catch (error) {
      console.log(
        "BOOKING ERROR:",
        error.response?.data
      );

      alert(
        error.response?.data?.detail ||
          "Booking Failed"
      );
    }
  };

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "50px",
        color: "white",
      }}
    >
      <h1>Search Train</h1>

      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="From Station"
          value={source}
          onChange={(e) =>
            setSource(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="text"
          placeholder="To Station"
          value={destination}
          onChange={(e) =>
            setDestination(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="date"
          value={journeyDate}
          onChange={(e) =>
            setJourneyDate(e.target.value)
          }
        />

        <br />
        <br />

        <select
          value={selectedPassenger}
          onChange={(e) =>
            setSelectedPassenger(
              e.target.value
            )
          }
        >
          <option value="">
            Select Passenger
          </option>

          {passengers.map(
            (passenger) => (
              <option
                key={passenger.id}
                value={passenger.id}
              >
                {passenger.name}
              </option>
            )
          )}
        </select>

        <br />
        <br />

        <button type="submit">
          Search Train
        </button>
      </form>

      <br />

      {trains.length > 0 && (
        <div>
          <h2>Available Trains</h2>

          {trains.map((train, index) => (
            <div
              key={index}
              style={{
                border:
                  "1px solid gray",
                padding: "10px",
                margin:
                  "10px auto",
                width: "400px",
              }}
            >
              <p>
                <strong>
                  Train No:
                </strong>{" "}
                {train.train_no}
              </p>

              <p>
                <strong>
                  Train Name:
                </strong>{" "}
                {train.train_name}
              </p>

              <p>
                <strong>
                  Status:
                </strong>{" "}
                {train.available
                  ? "Available ✅"
                  : "Not Available ❌"}
              </p>

              <button
                onClick={() =>
                  bookTrain(train)
                }
                disabled={
                  !train.available
                }
              >
                Book Now
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchTrain;