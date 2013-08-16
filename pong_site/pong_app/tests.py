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
    
    def test_make_user_get(self):
        response = self.client.get("/make_user/")
        self.assertEqual(response.status_code, 200)

    def test_make_user_post(self):
        response = self.client.post("/make_user/")
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
                          
    def test_update_user_get(self):
        response = self.client.get("/update_user/")
        self.assertEqual(response.status_code, 200)

    def test_update_user_post(self):
        response = self.client.post("/update_user/")
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

    def test_add_user_to_team_get(self):
        response = self.client.get("/add_user_to_team/")
        self.assertEqual(response.status_code, 200)

    def test_add_user_to_team_post(self):
        response = self.client.post("/add_user_to_team/")
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
                
    def test_user_profile_get(self):
        response = self.client.get("/user_profile/")
        self.assertEqual(response.status_code, 200)
        
    def test_user_profile_post(self):
        response = self.client.post("/user_profile/")
        self.assertEqual(response.status_code, 200)          
