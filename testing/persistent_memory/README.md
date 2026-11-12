# LangGraph Read Measurements & make decisions with persistent memory

LangGraph flow:
START -> observe -> decide -> execute -> observe.... -> END

Utilises MCP tool in SrsRAN reader app and gets a summary of the measurements. Stores in SQLite database.
Decisions stored in database along with what observation they were made on.
decision is a deterministic example on BLER right now
execution checks the proposed action in the decision and returns a dictionary, at the moment this is just a simulated execution status, with the result stored in the sqlite database along with the observations and decisions.
After execution it loops back to observe, this happens the amount of times specified by the script