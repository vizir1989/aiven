from parser.parser import parse
import pytest
from unittest.mock import MagicMock, Mock, patch
from requests import Response
from datetime import timedelta


@pytest.mark.parametrize(('url', 'status_code', 'elapsed', 'text', 'patterns', 'result'),
                         (('http://test.com', 200, 12345, 'it is testasdf', ['test'], ['test']),
                         ('http://test.com', 404, 12345, 'Page Not Found', [], []),
                         ('http://test.com', 200, 12345, 'hi 13245, hi', ['\\d+'], ['13245']),
                         ('test.com', 0, 0, '', ['\\d+'], [])))
def test_parser(url, status_code, elapsed, text, patterns, result):
    mock_context = MagicMock()
    mock_response = Mock(spec=Response)
    mock_response.elapsed = timedelta(microseconds=elapsed)
    mock_response.text = text
    mock_response.status_code = status_code
    mock_context.__enter__.return_value = mock_response

    with patch("requests.get", return_value=mock_context):
        result_status_code, result_elapsed, result_text = parse(url, patterns)
        assert result_status_code == status_code
        assert result_elapsed == elapsed
        assert result_text == result

