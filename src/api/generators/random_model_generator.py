import random
import uuid
from datetime import datetime, timedelta
from typing import get_type_hints, Any, get_origin, Annotated, get_args, Union
from datetime import date, timedelta


import rstr

from src.api.generators.generating_rule import GeneratingRule
class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, GeneratingRule):
                        rule = ann

            if field_name == "birthdate" and actual_type is str:
                days_ago = random.randint(0, 365 * 90)
                d = date.today() - timedelta(days=days_ago)
                init_data[field_name] = d.isoformat()
                continue

            if rule:
                value = RandomModelGenerator._generate_from_regex(
                    rule.regex,
                    actual_type
                )
            else:
                value = RandomModelGenerator._generate_value(actual_type)
            init_data[field_name] = value
        return cls(**init_data)


    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)

        if field_type is int:
            return int(generated)

        if field_type is float:
            return float(generated)

        return generated

    @staticmethod
    def _generate_value(field_type: Any) -> Any:
        origin = get_origin(field_type)

        # Optional[T] -> Union[T, NoneType]
        if origin is Union:
            args = [a for a in get_args(field_type)]
            non_none = [a for a in args if a is not type(None)]
            # чаще генерим значение, иногда None
            if not non_none or random.random() < 0.2:
                return None
            return RandomModelGenerator._generate_value(non_none[0])

        # List[T]
        if origin in (list,):
            (item_type,) = get_args(field_type) or (str,)
            # для REST-запроса на создание обычно достаточно 1 элемента
            return [RandomModelGenerator._generate_value(item_type)]

        # базовые типы
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(0, 1000)
        elif field_type is float:
            return round(random.uniform(0, 100.0), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is datetime:
            return datetime.now() - timedelta(seconds=random.randint(0, 100000))

        # вложенные модели (Pydantic)
        if isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)

        return None


