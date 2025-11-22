from src.utils import get_salary_value


def test_get_salary_value() -> None:
    """Тест для метода валидации зарплат"""
    assert get_salary_value(None) == 0
    assert get_salary_value({"from": 1000, "to": 2000}) == 1000
    assert get_salary_value({"to": 2000}) == 2000
    assert get_salary_value(1500) == 1500
    assert get_salary_value({}) == 0
