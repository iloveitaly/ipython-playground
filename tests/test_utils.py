import unittest
from unittest.mock import patch, MagicMock
from ipython_playground.utils import read_data_url


class TestUtils(unittest.TestCase):
    @patch("ipython_playground.utils.urlopen")
    def test_read_data_url_gist(self, mock_urlopen):
        # Mock the response
        mock_response = MagicMock()
        mock_response.read.return_value = b"gist data"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        url = "https://gist.github.com/user/123"
        result = read_data_url(url)

        # Check if URL was transformed
        expected_url = "https://gist.githubusercontent.com/user/123/raw"
        mock_urlopen.assert_called_with(expected_url)
        self.assertEqual(result, "gist data")

    @patch("ipython_playground.utils.urlopen")
    def test_read_data_url_regular(self, mock_urlopen):
        # Mock the response
        mock_response = MagicMock()
        mock_response.read.return_value = b"regular data"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        url = "https://example.com/data.txt"
        result = read_data_url(url)

        mock_urlopen.assert_called_with(url)
        self.assertEqual(result, "regular data")
