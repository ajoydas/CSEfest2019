import os
import pandas as pd
import datetime
import random
from faker import Faker
from pandas import ExcelWriter
fake = Faker('en_US')

EMAIL = {'example@gmail.com'}

CATEGORY = ('School', 'College')


def secret_gen():
    """Returns a random string of length string_length."""
    # random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    # random = random.upper()  # Make all characters uppercase.
    # random = random.replace("-", "")  # Remove the UUID '-'.
    # return random[0:6]  # Return the random string.


def main():
    """
    team name, name1, name2, name3, coach name, reg code
    :return:
    """
    timestamp = []
    for _ in range(10):
        timestamp.append(datetime.datetime.now())

    name = []
    for _ in range(10):
        name.append(fake.name())

    category = []
    for _ in range(10):
        category.append(random.sample(CATEGORY, 1))

    inst = []
    for _ in range(10):
        inst.append(fake.company())

    _email = []
    for _ in range(10):
        _email.append(random.sample(EMAIL, 1))


    _data_frame = {
        'timestamp': timestamp,
        'name': name,
        'category': category,
        'inst': inst,
        'email': _email,
    }

    df = pd.DataFrame(data=_data_frame)
    print(df['email'])

    writer = pd.ExcelWriter('Pandas-Example2.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    main()
