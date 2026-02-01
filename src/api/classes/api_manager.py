from src.api.steps.admin_steps import AdminSteps
from src.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, create_object: list):
        self.admin_steps = AdminSteps(create_object)
        self.user_steps = UserSteps(create_object)
