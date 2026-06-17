from pydantic import BaseModel


class TicketResponse(BaseModel):
    ticket_id: int
    pnr: str
    ticket_number: str