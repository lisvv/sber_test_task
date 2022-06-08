def get_normalized_month(month: int) -> str:
    if month == 0:
        return "менее месяца"
    elif month == 1:
        return f"{month} месяц"
    elif 1 < month < 5:
        return f"{month} месяца"
    elif month < 12:
        f"{month} месяцев"
    return "более года"
