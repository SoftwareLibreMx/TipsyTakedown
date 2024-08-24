from unittest.mock import patch

from shared.db_connection import get_db_engine


def test_db_connection():
    mock_create_engine = patch(
        'shared.db_connection.create_engine').start()

    get_db_engine('user', 'password', 'host', 'port', 'db_name')

    mock_create_engine.assert_called_with(
        'postgresql://user:password@host:port/db_name')
