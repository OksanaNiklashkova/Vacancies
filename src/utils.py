from typing import Dict, Optional, Union


def get_salary_value(salary: Optional[Union[int, float, Dict[str, Optional[Union[int, float]]]]]) -> Union[int, float]:
    """Метод для валидации зарплаты"""
    if salary is None:
        return 0
    elif isinstance(salary, dict):
        if salary.get("from") is not None:
            return salary["from"] or 0
        elif salary.get("to") is not None:
            return salary["to"] or 0
        else:
            return 0
    elif isinstance(salary, (int, float)):
        return salary
    return 0
