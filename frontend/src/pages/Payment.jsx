import { useState } from "react";
import axios from "axios";

function Payment() {
  const [bookingId, setBookingId] = useState("");
  const [amount, setAmount] = useState("");
  const [method, setMethod] = useState("UPI");
  const [message, setMessage] = useState("");

  const makePayment = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await axios.post(
        "http://127.0.0.1:8000/payment/pay",
        {
          booking_id: Number(bookingId),
          amount: Number(amount),
          payment_method: method,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage("✅ Payment Successful");
      console.log(res.data);
    } catch (err) {
      console.log(err);
      setMessage("❌ Payment Failed");
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
      <h1>Payment</h1>

      <input
        type="number"
        placeholder="Booking ID"
        value={bookingId}
        onChange={(e) => setBookingId(e.target.value)}
      />

      <br />
      <br />

      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <br />
      <br />

      <select
        value={method}
        onChange={(e) => setMethod(e.target.value)}
      >
        <option>UPI</option>
        <option>CARD</option>
        <option>NETBANKING</option>
      </select>

      <br />
      <br />

      <button onClick={makePayment}>
        Pay Now
      </button>

      <h3>{message}</h3>
    </div>
  );
}

export default Payment;