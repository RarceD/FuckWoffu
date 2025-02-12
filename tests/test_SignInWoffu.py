import unittest
from unittest.mock import patch
from src.SignInWoffu import SignInWoffu


class TestSignInWoffu(unittest.TestCase):

    @patch("src.SignInWoffu.requests.post")
    def test_get_token_success(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "fake_token"}
        mock_post.return_value = mock_response

        sign_in_woffu = SignInWoffu("test@example.com", "password", "company")
        token = sign_in_woffu._get_token("test@example.com", "password")

        self.assertEqual(token, "fake_token")
        mock_post.assert_called_with(
            "https://company.woffu.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "password",
                "username": "test@example.com",
                "password": "password",
            },
        )

    @patch("src.SignInWoffu.time.sleep")
    @patch("src.SignInWoffu.requests.post")
    def test_get_token_failure(self, mock_post, mock_sleep):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 401  # Simula un error de autenticación
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            SignInWoffu("test@example.com", "password", "company")

        self.assertIn("Failed to get token", str(context.exception))
        mock_post.assert_called_with(
            "https://company.woffu.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "password",
                "username": "test@example.com",
                "password": "password",
            },
        )


if __name__ == "__main__":
    unittest.main()
