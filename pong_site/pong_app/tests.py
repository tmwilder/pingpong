from django.test import TestCase
from django.test.client import Client


class StatusOkTests(TestCase):
    #Django test magic that goes and loads the listed fixtures.
    fixtures = ['initial_data.json']
    def setUp(self):
        self.client = Client()
        
    def test_index_get(self):
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
        
    def test_index_post(self):
        response = self.client.post("/index/")
        self.assertEqual(response.status_code, 200)        
        
    def test_enter_result_get(self):
        response = self.client.get("/enter_result/")
        self.assertEqual(response.status_code, 200)

    def test_enter_result_post(self):
        response = self.client.post("/enter_result/")
        self.assertEqual(response.status_code, 200)
    
    def test_make_player_get(self):
        response = self.client.get("/make_player/")
        self.assertEqual(response.status_code, 200)

    def test_make_player_post(self):
        response = self.client.post("/make_player/")
        self.assertEqual(response.status_code, 200)

    def test_make_team_get(self):
        response = self.client.get("/make_team/")
        self.assertEqual(response.status_code, 200)

    def test_make_team_post(self):
        response = self.client.post("/make_team/")
        self.assertEqual(response.status_code, 200)

    def test_make_league_get(self):
        response = self.client.get("/make_league/")
        self.assertEqual(response.status_code, 200)

    def test_make_league_post(self):
        response = self.client.post("/make_league/")
        self.assertEqual(response.status_code, 200)
                          
    def test_update_player_get(self):
        response = self.client.get("/update_player/")
        self.assertEqual(response.status_code, 200)

    def test_update_player_post(self):
        response = self.client.post("/update_player/")
        self.assertEqual(response.status_code, 200)

    def test_update_team_get(self):
        response = self.client.get("/update_team/")
        self.assertEqual(response.status_code, 200)

    def test_update_team_post(self):
        response = self.client.post("/update_team/")
        self.assertEqual(response.status_code, 200)

    def test_update_league_get(self):
        response = self.client.get("/update_league/")
        self.assertEqual(response.status_code, 200)

    def test_update_league_post(self):
        response = self.client.post("/update_league/")
        self.assertEqual(response.status_code, 200)

    def test_add_player_to_team_get(self):
        response = self.client.get("/add_player_to_team/")
        self.assertEqual(response.status_code, 200)

    def test_add_player_to_team_post(self):
        response = self.client.post("/add_player_to_team/")
        self.assertEqual(response.status_code, 200)

    def test_add_team_to_league_get(self):
        response = self.client.get("/add_team_to_league/")
        self.assertEqual(response.status_code, 200)
        
    def test_add_team_to_league_post(self):
        response = self.client.post("/add_team_to_league/")
        self.assertEqual(response.status_code, 200)
                                                                                          
    def test_team_profile_get(self):
        response = self.client.get("/team_profile/")
        self.assertEqual(response.status_code, 200)
        
    def test_team_profile_post(self):
        response = self.client.post("/team_profile/")
        self.assertEqual(response.status_code, 200)
                
    def test_player_profile_get(self):
        response = self.client.get("/player_profile/")
        self.assertEqual(response.status_code, 200)
        
    def test_player_profile_post(self):
        response = self.client.post("/player_profile/")
        self.assertEqual(response.status_code, 200)
                        
    def test_standings_get(self):
        response = self.client.get("/standings/")
        self.assertEqual(response.status_code, 200)
        
    def test_standings_post(self):
        response = self.client.post("/standings/")
        self.assertEqual(response.status_code, 200)
               
    def test_match_profile_get(self):
        response = self.client.get("/match_profile/")
        self.assertEqual(response.status_code, 200)  
        
    def test_match_profile_post(self):
        response = self.client.post("/match_profile/")
        self.assertEqual(response.status_code, 200)                
