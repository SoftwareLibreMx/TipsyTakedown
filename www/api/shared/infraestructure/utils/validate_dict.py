from dataclasses import dataclass


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
        if vk_option.required and vk_option.key not in data:
            errors.append(f'{vk_option.key} is required')

        if vk_option.key in data and not isinstance(data[vk_option.key], vk_option.type):
            errors.append(f'{vk_option.key} must be of type {vk_option.type}')

        if vk_option.options and data[vk_option.key] not in vk_option.options:
            errors.append(f'{vk_option.key} must be in {vk_option.options}')

    return errors
