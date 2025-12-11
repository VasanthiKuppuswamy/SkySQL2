import flights_data
from datetime import datetime
import sqlalchemy

IATA_LENGTH = 3


def delayed_flights_by_airline():
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("Enter airline name: ")
    results = flights_data.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport():
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_airport".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Valide input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = flights_data.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id():
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = flights_data.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date():
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = flights_data.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    """
    Get a list of flight results (List of dictionary-like objects from SQLAachemy).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    Optionally the results exports to CSV.
    """
    if not results:
      return
    print(f"Got {len(results)} results.")
    for result in results:
        formatted_result = []
    
        result = result._mapping

        
        try:
            delay = int(result['DELAY']) if result['DELAY'] else 0  # If delay columns is NULL, set it to 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
            flight_id = result['ID']

         
            formatted_result.append({
                'ID': flight_id,
                'ORIGIN': origin,
                'DESTINATION': dest,
                'AIRLINE': airline,
                'DELAY': delay
            })

        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        if delay and delay > 0:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")

    
    if formatted_result:
        ask_to_save_data(formatted_result)


def ask_to_save_data(data):
    """
    Ask user if they want to save data to CSV file.
    If yes, prompt for filename and save the data.
    """
    export_choice = input("Would you like to export this data to a CSV file? (y/n): ").strip().lower()
    if export_choice == 'y':
        filename = input("Enter filename (e.g., delayed_flights.csv): ").strip()
        if not filename.endswith('.csv'):
            filename += '.csv'
        save_to_csv(data, filename)


def save_to_csv(data, filename):
    """
    Save flight data to a CSV file with the given filename.
    """
    try:
        with open(filename, 'w') as fileobj:
            # Write header
            fileobj.write("Flight ID,Origin Airport,Destination Airport,Airline,Delay (Minutes)\n")

            # Write data rows
            for row in data:
                fileobj.write(f"{row['ID']},{row['ORIGIN']},{row['DESTINATION']},{row['AIRLINE']},{row['DELAY']}\n")

        print(f"Data successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("Try again...")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = { 1: (flight_by_id, "Show flight by ID"),
              2: (flights_by_date, "Show flights by date"),
              3: (delayed_flights_by_airline, "Delayed flights by airline"),
              4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
              5: (quit, "Exit")
             }


def main():

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func()


if __name__ == "__main__":
    main()