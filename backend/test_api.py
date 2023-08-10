#==gonna write our unit tests from here
import unittest
from main import create_app
from config import TestConfig
from exts import db
#NOW actually writing my unittests

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)

        self.client=self.app.test_client(self)
        #this is the client
        #have to be within the app context
        with self.app.app_context():
            #db.init_app(self.app) #no need to call this again
            db.create_all()

    def test_hello_world(self):
        hellow_response = self.client.get('/recipe/hello')
        json = hellow_response.json

        print(json)

        self.assertEqual(json, {"message":"Hello World"})

    def test_signup(self):
        signup_response=self.client.post('/auth/signup',
            json={
                "username":"testuser",
                "email":"testuser@test.com",
                "password":"password"
            }
        )
        #we very well know that this mthd is supposed to 
        #return a status code of 201
        status_code = signup_response.status_code
        self.assertEqual(status_code,201)
    def test_login(self):
        signup_response=self.client.post('/auth/login',
            json={
                "username":"testuser",
                "email":"testuser@test.com",
                "password":"password"
            }
        )
        login_response=self.client.post('/auth/login',
            json={
                "username":"testuser",
                "email":"testuser@test.com",
            }
        )
        status_code = login_response.status_code
        self.assertEqual(status_code,200)

    def test_get_all_recipes(self):
        """TEST GETTING ALL RECIPES"""
        response = self.client.get('/recipe/recipes')
        #print(response.json)
        status_code=response.status_code
        self.assertEqual(status_code,200)

    def test_get_one_recipe(self):
        id=1
        response=self.client.get(f'/recipes/recipe/{id}')
        
        status_code = response.status_code
        self.assertEqual(status_code, 404) #404 because we dont have anything in db
    def test_create_recipe(self):
        signup_response=self.client.post('/auth/login',
            json={
                "username":"testuser",
                "email":"testuser@test.com",
                "password":"password"
            }
        )
        login_response=self.client.post('/auth/login',
            json={
                "username":"testuser",
                "email":"testuser@test.com",
            }
        )
        access_token  = login_response["access_token"]
        create_recipe_response=self.client.post(
            '/recipe/recipes',
            json={
                "title":"Test Cookie",
                "description":"Test description"
            },
            headers = {
                "Authorization":f"Bearer {access_token}"
            }
        )
        status_code = create_recipe_response.status_code
        get_one = self.client.get(f'/recipe/recipe/{id}')
        print(get_one.json)
        self.assertEqual(status_code, 201)


    def test_update_recipe(self):
        pass

    def test_delete_recipe(self):
        pass


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()#this runs our test runner