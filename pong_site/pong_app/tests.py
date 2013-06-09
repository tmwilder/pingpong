from django.test import TestCase
from django.test.client import Client


class StatusOkTests(TestCase):
    #Django test magic that goes and loads the listed fixtures.
    fixtures = ['initial_data.json']
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        response = self.client.post("/index/")
        self.assertEqual(response.status_code, 200)
        
    def test_enter_result(self):
        response = self.client.post("/enter_result/")
        self.assertEqual(response.status_code, 200)
        
    def test_make_player(self):
        response = self.client.post("/make_player/")
        self.assertEqual(response.status_code, 200)

    def test_make_team(self):
        response = self.client.post("/make_team/")
        self.assertEqual(response.status_code, 200)

    def test_make_league(self):
        response = self.client.post("/make_league/")
        self.assertEqual(response.status_code, 200)
                                
    def test_update_player(self):
        response = self.client.post("/update_player/")
        self.assertEqual(response.status_code, 200)
    
    def test_update_team(self):
        response = self.client.post("/update_team/")
        self.assertEqual(response.status_code, 200)

    def test_update_league(self):
        response = self.client.post("/update_league/")
        self.assertEqual(response.status_code, 200)

    def test_add_player_to_team(self):
        response = self.client.post("/add_player_to_team/")
        self.assertEqual(response.status_code, 200)

    def test_add_team_to_league(self):
        response = self.client.post("/add_team_to_league/")
        self.assertEqual(response.status_code, 200)
                                                                                           
    def test_team_profile(self):
        response = self.client.post("/team_profile/")
        self.assertEqual(response.status_code, 200)
        
    def test_player_profile(self):
        response = self.client.post("/player_profile/")
        self.assertEqual(response.status_code, 200)
                
    def test_standings(self):
        response = self.client.post("/standings/")
        self.assertEqual(response.status_code, 200)
        
    def test_match_profile(self):
        response = self.client.post("/match_profile/")
        self.assertEqual(response.status_code, 200)                
