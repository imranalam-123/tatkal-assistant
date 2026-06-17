import { useState, useEffect } from "react";
import api from "../services/api";

function PassengerDetails() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [berthPreference, setBerthPreference] =
    useState("");

  const [passengers, setPassengers] = useState([]);

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

      setPassengers(response.data);

    } catch (error) {
      console.log(error);
    }
  };

  const addPassenger = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await api.post(
        "/passenger/add",
        {
          name,
          age: Number(age),
          gender,
          berth_preference: berthPreference,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Passenger Added Successfully");

      setName("");
      setAge("");
      setGender("");
      setBerthPreference("");

      fetchPassengers();

    } catch (error) {
      console.log(error);
      alert("Failed To Add Passenger");
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
      <h1>Passenger Details</h1>

      <form onSubmit={addPassenger}>
        <input
          type="text"
          placeholder="Passenger Name"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) =>
            setAge(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="text"
          placeholder="Gender"
          value={gender}
          onChange={(e) =>
            setGender(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="text"
          placeholder="Berth Preference"
          value={berthPreference}
          onChange={(e) =>
            setBerthPreference(
              e.target.value
            )
          }
        />

        <br />
        <br />

        <button type="submit">
          Add Passenger
        </button>
      </form>

      <br />

      <h2>Saved Passengers</h2>

      {passengers.map((passenger) => (
        <div
          key={passenger.id}
          style={{
            border: "1px solid gray",
            width: "500px",
            margin: "10px auto",
            padding: "10px",
          }}
        >
          <p>
            <strong>Name:</strong>{" "}
            {passenger.name}
          </p>

          <p>
            <strong>Age:</strong>{" "}
            {passenger.age}
          </p>

          <p>
            <strong>Gender:</strong>{" "}
            {passenger.gender}
          </p>

          <p>
            <strong>Berth:</strong>{" "}
            {passenger.berth_preference}
          </p>
        </div>
      ))}
    </div>
  );
}

export default PassengerDetails;