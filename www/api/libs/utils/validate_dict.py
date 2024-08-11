from dataclasses import dataclass
from enum import Enum


@dataclass
class VKOptions:
    key: str = None
    type: type = None
    required: bool = False
    default: any = None
    options: list = None


def validate_dict(data: dict, vk_options: list[VKOptions]) -> list[str]:
    errors = []

    for vk_option in vk_options:
        if vk_option.key not in data and vk_option.default:
            data[vk_option.key] = vk_option.default
            continue

        if vk_option.required and vk_option.key not in data:
            errors.append(f'{vk_option.key} is required')

        valid_enum_value = (
            issubclass(vk_option.type, Enum)
            and data[vk_option.key] not in vk_option.type
        )
        is_instance = isinstance(data[vk_option.key], vk_option.type)
        if vk_option.key in data and (not enum_value or not is_instance):
            errors.append(f'{vk_option.key} must be of type {vk_option.type}')

        if vk_option.options and data[vk_option.key] not in vk_option.options:
            errors.append(f'{vk_option.key} must be in {vk_option.options}')

    return errors
