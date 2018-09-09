from datetime import datetime, timedelta, date
import string


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def clean(row):
    clean = []
    for word in row.split(' '):
        filtered = remove_punctuation(word)
        if len(filtered) > 0:
            clean.append(remove_punctuation(word))
    else:
        return clean


def get_year_and_month():
    now = datetime.now()
    today = now.date()
    year = today.year
    month = today.month
    return year, month
