# pylint: disable=unused-variable,expression-not-assigned

from unittest.mock import patch, call, Mock

import pytest
from expecter import expect

from memegen.factory import create_app
from memegen.settings import get_config
from memegen.routes._utils import display


def describe_display():

    @pytest.fixture
    def app():
        app = create_app(get_config('test'))
        app.config['GOOGLE_ANALYTICS_TID'] = 'my_tid'
        return app

    request_image = Mock(url="it's a path")
    request_image.headers.get = Mock(return_value="(not a browser)")
    request_image.base_url = "it's a path"
    request_image.args = {}

    request_share = Mock(url="it's a path?alt=style&share=true")
    request_share.headers.get = Mock(return_value="*/*")
    request_share.base_url = "it's a path"
    request_share.args = {'alt': ['style'], 'share': ['true']}

    @patch('memegen.routes._utils.send_file')
    @patch('memegen.routes._utils.request', request_image)
    def it_returns_an_image_otherwise(mock_send_file, app):
        with app.test_request_context():
            display("my_title", "my_path")

        expect(mock_send_file.mock_calls) == [
            call("my_path", mimetype='image/jpeg'),
        ]

    @patch('memegen.routes._utils.request', request_share)
    def it_returns_html_when_sharing(app):
        with app.test_request_context():
            html = display("my_title", "my_path", share=True, raw=True)

        print(html)
        assert "<title>my_title</title>" in html
        assert 'src="it\'s a path?alt=style"' in html
        assert "ga('create', 'my_tid', 'auto');" in html
