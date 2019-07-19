from datetime import datetime, timezone

def ISO8601_to_UTC(datetime_string):
    try:
        datetime_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError as e:
        raise(e)
    # convert localtime to UTC
    datetime_object = datetime_object.replace(tzinfo=timezone.utc) - datetime_object.utcoffset()
    return datetime_object