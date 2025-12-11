from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = """
SELECT 
    flights.ID as ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline as AIRLINE,
    flights.DEPARTURE_DELAY as DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.ID = :id
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT 
    flights.ID as ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline as AIRLINE,
    flights.DEPARTURE_DELAY as DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE DAY = :day AND MONTH = :month AND YEAR = :year
"""

QUERY_DELAYED_BY_AIRLINE = """
SELECT 
    flights.ID as ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline as AIRLINE,
    flights.DEPARTURE_DELAY as DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE airlines.airline LIKE :airline 
  AND flights.DEPARTURE_DELAY >= 20 
  AND flights.DEPARTURE_DELAY IS NOT NULL 
ORDER BY flights.DEPARTURE_DELAY DESC
"""

QUERY_DELAYED_BY_AIRPORT = """
SELECT 
    flights.ID as ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline as AIRLINE,
    flights.DEPARTURE_DELAY as DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.ORIGIN_AIRPORT = :airport 
  AND flights.DEPARTURE_DELAY >= 20  -- Only delays of 20+ minutes
  AND flights.DEPARTURE_DELAY IS NOT NULL  -- Exclude NULL values
ORDER BY flights.DEPARTURE_DELAY DESC
"""


# Define the database URL
DATABASE_URL = "sqlite:///data/flights.sqlite3"

# Create the engine
engine = create_engine(DATABASE_URL)

def execute_query(query, params):
    """
    Execute an SQL query with the params provided in a dictionary,
    and returns a list of records (dictionary-like objects).
    If an exception was raised, print the error, and return an empty list.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.fetchall()
    except Exception as e:
        print("Query error:", e)
        return []

def get_flight_by_id(flight_id):
    """
    Searches for flight details using flight ID.
    If the flight was found, returns a list with a single record.
    """
    params = {'id': flight_id}
    return execute_query(QUERY_FLIGHT_BY_ID, params)

def get_flights_by_date(day, month, year):
    """
    Searches for flight details using DAY, MONTH, YEAR.
    """
    params = {
        'day': day,
        'month': month,
        'year': year
    }
    return execute_query(QUERY_FLIGHTS_BY_DATE, params)


def get_delayed_flights_by_airline(airline_name):
    """
    Searches for delayed airlines (20+ mins) details using airline name.
    """
    params = {'airline': f'%{airline_name}%'}
    return execute_query(QUERY_DELAYED_BY_AIRLINE, params)

def get_delayed_flights_by_airport(airport_code):
    """
    Search delayed flights (20+ mins) by origin airport
    """
    params = {'airport': airport_code.upper()}
    return execute_query(QUERY_DELAYED_BY_AIRPORT, params)