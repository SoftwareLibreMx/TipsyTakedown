import inspect
from dataclasses import dataclass
from enum import Enum


@dataclass
class VKOptions:
    key: str = None
    type: type = None
    required: bool = False
    default: any = None
    options: list = None


def __is_invalid_type(vk_option, data):
    valid_enum_value = (
        inspect.isclass(vk_option.type) and
        issubclass(vk_option.type, Enum)
        and data[vk_option.key] in vk_option.type
    )

    is_instance = data.get(vk_option.key, None) and isinstance(
        data[vk_option.key], vk_option.type)

    return not valid_enum_value and not is_instance


def validate_dict(data: dict, vk_options: list[VKOptions]) -> list[str]:
    errors = []

    for vk_option in vk_options:
        if vk_option.key not in data and vk_option.default:
            data[vk_option.key] = vk_option.default
            continue

        strEmpty = data.get(vk_option.key, None) == ''
        anyNone = data.get(vk_option.key, None) is None
        if vk_option.required and (strEmpty or anyNone):
            errors.append(f'{vk_option.key} is required')

        invalid_type = __is_invalid_type(vk_option, data)
        if vk_option.key in data and data[vk_option.key] and invalid_type:
            errors.append(f'{vk_option.key} must be of type {vk_option.type}')

        if vk_option.options and data[vk_option.key] not in vk_option.options:
            errors.append(f'{vk_option.key} must be in {vk_option.options}')

    return errors
