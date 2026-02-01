import string

from faker import Faker
import random

#TODO: почему это костыль?
class RandomData:
    faker = Faker()

    @staticmethod
    def get_valid_username() -> str:
        length = random.randint(3, 15)
        return "".join(
            RandomData.faker.random_letters(length=length))

    @staticmethod
    def get_valid_password() -> str:
        upper = random.sample(string.ascii_uppercase, 3)
        lower = random.sample(string.ascii_lowercase, 3)
        digits = random.sample(string.digits, 3)
        special = random.choice("!@#$%")

        pwd = upper + lower + digits + [special]
        random.shuffle(pwd)
        return "".join(pwd)