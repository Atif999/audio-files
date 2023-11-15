import unittest
from flask import Flask
from io import BytesIO
from app import app

class TestAudioAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_post_audio(self):
        response = self.app.post('/audio', data={'file': (BytesIO(b'Test data'), 'test.txt')},
                                 headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
        self.assertEqual(response.status_code, 201)

    def test_get_audio_json(self):
        # First, post an audio file
        self.app.post('/audio', data={'file': (BytesIO(b'Test data'), 'test.txt')},
                      headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})

        # Then, get the audio data as JSON
        response = self.app.get('/audio/1', headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.get_json())
        self.assertIn('filename', response.get_json())
        self.assertIn('data', response.get_json())

    def test_get_audio_file(self):
        # First, post an audio file
        self.app.post('/audio', data={'file': (BytesIO(b'Test data'), 'test.txt')},
                      headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})

        # Then, get the audio file
        response = self.app.get('/audio/1?file=true', headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'audio/wav')

    def tearDown(self):
        pass  # Clean up if needed

if __name__ == '__main__':
    unittest.main()
