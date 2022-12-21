from user_model import UserModel


def bmi(user: UserModel):
    return user.weight / (user.height / 100) ** 2  # kg/m
