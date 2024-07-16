import pytest
import unittest

from .validate_dict import validate_dict, VKOptions


@pytest.mark.parametrize('data, vk_options, expected', [
    ({'name': 'John Doe'}, [VKOptions('name', str, True)], []),  # No errors
    ({}, [VKOptions('name', str, True)], ['name is required']),  # Required field
    ({'name': 123}, [VKOptions('name', str, True)], ['name must be of type <class \'str\'>']),  # Type error
    ({'name': 'John Doe'}, [VKOptions('name', str, True, options=['John Doe'])], []),  # No errors
    ({'name': 'Jane Doe'}, [VKOptions('name', str, True, options=['John Doe'])], ['name must be in [\'John Doe\']'])  # Options error
])
def test_validate_errors(data, vk_options, expected):
    assert validate_dict(data, vk_options) == expected


@pytest.mark.parametrize('data, vk_options, expected', [
    ({}, [VKOptions('name', str, default='John Doe')], {'name': 'John Doe'}),  # Default value
    ({'name': 'John Doe'}, [VKOptions('name', str, default='Jane Doe')], {'name': 'John Doe'}),  # No errors
])
def test_validate_data(data, vk_options, expected):
    validate_dict(data, vk_options)

    assert data == expected
