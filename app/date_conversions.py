def convert_to_mysql_datetime(iso_datetime):
    """
    Convert an ISO 8601 datetime string (e.g., '2024-11-26T17:06:39.104Z') to MySQL datetime format (YYYY-MM-DD HH:MM:SS).
    """
    # Remove 'Z' (UTC) and replace with '+00:00' for correct parsing
    iso_datetime = iso_datetime.replace("Z", "+00:00")

    # Parse the ISO datetime string into a Python datetime object
    datetime_obj = datetime.fromisoformat(iso_datetime)

    # Convert to MySQL format: 'YYYY-MM-DD HH:MM:SS'
    return datetime_obj.strftime('%Y-%m-%d %H:%M')


from datetime import datetime


def mysql_to_iso(mysql_datetime):
    """Converts MySQL DATETIME to ISO 8601 format."""
    try:
        # Check if the input is already a datetime object
        if isinstance(mysql_datetime, datetime):
            return mysql_datetime.isoformat()  # Convert directly to ISO format

        # If it's a string, parse it using the known format
        elif isinstance(mysql_datetime, str):
            dt = datetime.strptime(mysql_datetime, '%Y-%m-%d %H:%M')
            return dt.isoformat()

        # Handle None gracefully
        elif mysql_datetime is None:
            return None

        # Unexpected type fallback
        return None
    except Exception as e:
        print(f"Error in mysql_to_iso: {e}")
        return None



