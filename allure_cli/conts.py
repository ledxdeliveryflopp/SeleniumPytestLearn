from dataclasses import dataclass


class EXECUTION:
    """Список исполнителей в Allure"""
    types: dict = {"jenkins": "jenkins", "bamboo": "bamboo", "teamcity": "teamcity", "gitlab": "gitlab",
                   "github": "github", "circleci": "circleci", "bitbucket": "bitbucket"}


@dataclass
class AllureConst:
    executor_type: EXECUTION


executors_const = AllureConst(executor_type=EXECUTION())
