# LangGraph Read Measurements & make decisions with persistent memory

LangGraph flow:
START -> observe -> decide -> END

Utilises MCP tool in SrsRAN reader app and gets a summary of the measurements. Stores in SQLite database.
Decisions stored in database along with what observation they were made on.
decision is a deterministic example on BLER right now

Every run appends 2 observations to the database