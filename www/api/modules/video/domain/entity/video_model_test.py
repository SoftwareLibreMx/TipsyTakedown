import pytest

from .video_model import VideoModel


@pytest.mark.unit
def test_from_dict():
    mock_video_dict = {
        'teacher_id': '123',
        'name': 'Video 1',
        'description': 'Description 1',
    }

    expected_video = VideoModel(
        teacher_id='123',
        name='Video 1',
        description='Description 1',
    )

    errors, video = VideoModel.from_dict(mock_video_dict)

    assert errors is None

    assert video.teacher_id == expected_video.teacher_id
    assert video.name == expected_video.name
    assert video.description == expected_video.description
