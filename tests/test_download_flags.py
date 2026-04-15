import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import download_flags


class DownloadFlagsTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        download_flags.FLAGS_DIR = Path(self.tempdir.name)
        download_flags.FLAGS_DIR.mkdir(parents=True, exist_ok=True)
        download_flags.COUNTRY_CODES = {"testland": "tl"}

    @patch("download_flags.requests.get")
    def test_skips_download_when_file_exists(self, mock_get):
        (download_flags.FLAGS_DIR / "testland.png").write_bytes(b"cached")
        download_flags.download_flags()
        mock_get.assert_not_called()

    @patch("download_flags.requests.get")
    def test_downloads_and_saves_flag_image(self, mock_get):
        response = Mock()
        response.content = b"image-bytes"
        response.raise_for_status = Mock()
        mock_get.return_value = response

        download_flags.download_flags()

        expected = download_flags.FLAGS_DIR / "testland.png"
        self.assertTrue(expected.exists())
        self.assertEqual(expected.read_bytes(), b"image-bytes")
        mock_get.assert_called_once_with(
            "https://flagcdn.com/w640/tl.png",
            headers=download_flags.HEADERS,
            timeout=10,
        )

    @patch("download_flags.requests.get")
    def test_handles_request_failure_without_crashing(self, mock_get):
        mock_get.side_effect = RuntimeError("network down")
        download_flags.download_flags()
        self.assertFalse((download_flags.FLAGS_DIR / "testland.png").exists())


if __name__ == "__main__":
    unittest.main()
