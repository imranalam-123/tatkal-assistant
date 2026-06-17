import { useEffect, useState } from "react";
import api from "../services/api";

function Tickets() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get(
        "/ticket/all",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("TICKETS:", response.data);

      setTickets(response.data);

    } catch (error) {
      console.log(error);
      alert("Failed to Load Tickets");
    }
  };

  const downloadTicket = async (ticketId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get(
        `/ticket/download/${ticketId}`,
        {
          responseType: "blob",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );

      const link = document.createElement("a");

      link.href = url;
      link.setAttribute(
        "download",
        `ticket_${ticketId}.pdf`
      );

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.log(error);
      alert("Download Failed");
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
      <h1>My Tickets</h1>

      {tickets.length === 0 ? (
        <p>No Tickets Found</p>
      ) : (
        tickets.map((ticket) => (
          <div
            key={ticket.id}
            style={{
              border: "1px solid gray",
              margin: "10px auto",
              padding: "15px",
              width: "500px",
            }}
          >
            <p>
              <strong>Ticket Number:</strong>{" "}
              {ticket.ticket_number}
            </p>

            <p>
              <strong>PNR:</strong>{" "}
              {ticket.pnr}
            </p>

            <button
              onClick={() =>
                downloadTicket(ticket.id)
              }
              style={{
                padding: "8px 15px",
                cursor: "pointer",
              }}
            >
              Download PDF
            </button>
          </div>
        ))
      )}
    </div>
  );
}

export default Tickets;