from datetime import datetime, timedelta

def generate_dates_between(start_date_str, end_date_str):
    """Generate a list of date strings between two date strings."""
    
    start_date_str = str(start_date_str)
    end_date_str = str(end_date_str)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    interval = timedelta(days=1)
    dates = []
    
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))  # Format as 'YYYY-%m-%d'
        current_date += interval
    
    return dates



def get_itin(itinerary_data):
    """ Create a dictionary to store the itinerary data by date and hour."""
    itinerary_dict = {}

    for itinerary_entry in itinerary_data:
        date = itinerary_entry.date
        hour = itinerary_entry.hour
        val = itinerary_entry.val

        if date not in itinerary_dict:
            itinerary_dict[date] = {}

        itinerary_dict[date][hour] = val

    return itinerary_dict


