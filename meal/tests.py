from django.db.models import Sum
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from reporter.models import Reporter
from .models import Meal

from datetime import datetime, timedelta


class MealModelTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="username1_correct")
        user1.set_password("password1_correct")
        user1.save()
        reporter1 = Reporter.objects.create(user=user1)
        
        user2 = User.objects.create(username="username2_correct")
        user2.set_password("password2_correct")
        user2.save()
        reporter2 = Reporter.objects.create(user=user2)
        
        now = datetime(2016, 7, 21, 14, 30)
        date = now.date()
        time = now.time()
        timedeltaH1 = timedelta(hours=1)
        timedeltaH2 = timedelta(hours=2)
        timedeltaH3 = timedelta(hours=3)
        timedeltaD1 = timedelta(days=1)
        timedeltaD2 = timedelta(days=2)
        timedeltaD3 = timedelta(days=3)
        
        Meal.objects.create(reporter=reporter1, description="meal11", calories=100, date=date, time=time)
        Meal.objects.create(reporter=reporter1, description="meal12", calories=200, date=date-timedeltaD1, time=time)
        Meal.objects.create(reporter=reporter1, description="meal13", calories=300, date=date-timedeltaD2, time=time)
        Meal.objects.create(reporter=reporter1, description="meal14", calories=400, date=date-timedeltaD3, time=time)
        Meal.objects.create(reporter=reporter1, description="meal15", calories=90, date=date, time=(now-timedeltaH1).time())
        Meal.objects.create(reporter=reporter1, description="meal16", calories=80, date=date, time=(now-timedeltaH2).time())
        Meal.objects.create(reporter=reporter1, description="meal17", calories=70, date=date, time=(now-timedeltaH3).time())
        
        Meal.objects.create(reporter=reporter2, description="meal21", calories=100, date=date, time=time)
        Meal.objects.create(reporter=reporter2, description="meal22", calories=200, date=date-timedeltaD2, time=time)
        Meal.objects.create(reporter=reporter2, description="meal33", calories=300, date=date+timedeltaD2, time=time)
        Meal.objects.create(reporter=reporter2, description="meal51", calories=90, date=date, time=(now-timedeltaH1).time())
        Meal.objects.create(reporter=reporter2, description="meal61", calories=80, date=date, time=(now+timedeltaH1).time())
        Meal.objects.create(reporter=reporter2, description="meal51", calories=70, date=date, time=(now-timedeltaH2).time())
        Meal.objects.create(reporter=reporter2, description="meal61", calories=60, date=date, time=(now+timedeltaH2).time())
        Meal.objects.create(reporter=reporter2, description="meal51", calories=50, date=date, time=(now-timedeltaH3).time())
        Meal.objects.create(reporter=reporter2, description="meal61", calories=40, date=date, time=(now+timedeltaH3).time())

    def test_meal(self):
        reporter1 = Reporter.objects.get(user=User.objects.get(username="username1_correct"))
        reporter2 = Reporter.objects.get(user=User.objects.get(username="username2_correct"))
        
        now = datetime(2016, 7, 21, 14, 30)
        date = now.date()
        time = now.time()
        
        meals1 = Meal.objects.filter(reporter=reporter1)
        self.assertEqual(meals1.count(), 7)
        meals2 = Meal.objects.filter(reporter=reporter2)
        self.assertEqual(meals2.count(), 9)
        
        meals1 = meals1.filter(date=date)
        self.assertEqual(meals1.count(), 4)
        meals2 = meals2.filter(date=date)
        self.assertEqual(meals2.count(), 7)
        
        calories1 = meals1.aggregate(Sum('calories'))
        self.assertEqual(calories1['calories__sum'], 340)
        calories2 = meals2.aggregate(Sum('calories'))
        self.assertEqual(calories2['calories__sum'], 490)


class MealAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        user = User.objects.create(username="username1_correct")
        user.set_password("password1_correct")
        user.save()
        reporter = Reporter.objects.create(user=user, role=3)
        
        user = User.objects.create(username="username2_correct")
        user.set_password("password2_correct")
        user.save()
        reporter = Reporter.objects.create(user=user)

    def test_meal_crud(self):
        now = datetime(2016, 7, 21, 14, 30)
        date = now.date()
        time = now.time()
        timedeltaH1 = timedelta(hours=1)
        timedeltaH2 = timedelta(hours=2)
        timedeltaH3 = timedelta(hours=3)
        timedeltaD1 = timedelta(days=1)
        timedeltaD2 = timedelta(days=2)
        timedeltaD3 = timedelta(days=3)

        ## post
        response = self.client.post("/api/v1/meal/", '{"reporter": 1, "description": "meal1", "calories": 100, "date": , "time": ""}', 'application/json')
        self.assertEqual(response.status_code, 403)
        
        response = self.client.post("/api/v1/auth/", '{"username": "username2_correct", "password": "password2_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal1", "calories": 100, "date": "", "time": ""}', 'application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal1", "calories": 100, "date": "2015-21-7", "time": ""}', 'application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal1", "calories": 100, "date": "", "time": "14:30"}', 'application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal1", "calories": 100, "date": "2015-21-7", "time": "14:30"}', 'application/json')
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal1", "calories": 100, "date": "2015-7-21", "time": "14:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal2", "calories": 200, "date": "2015-7-20", "time": "12:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/v1/meal/", '{"description": "meal3", "calories": 300, "date": "2015-7-21", "time": "10:30:01"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        # anyway will be added to reporter2
        response = self.client.post("/api/v1/meal/", '{"reporter": 1, "description": "meal4", "calories": 400, "date": "2015-7-21", "time": "11:30:01"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        # sign in as admin
        response = self.client.delete("/api/v1/auth/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/v1/auth/", '{"username": "username1_correct", "password": "password1_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        # will be added to reporter1
        response = self.client.post("/api/v1/meal/", '{"description": "meal1", "calories": 100, "date": "2015-7-21", "time": "6:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        # will be added to reporter2
        response = self.client.post("/api/v1/meal/", '{"reporter": 2, "description": "meal5", "calories": 500, "date": "2015-7-21", "time": "16:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        # will be added to reporter1
        response = self.client.post("/api/v1/meal/", '{"reporter": 1, "description": "meal2", "calories": 200, "date": "2015-7-19", "time": "6:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        ## get
        response = self.client.get("/api/v1/meal/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        response = self.client.get("/api/v1/meal/?reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        
        response = self.client.get("/api/v1/meal/?start_date=2015-7-20")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)
        response = self.client.get("/api/v1/meal/?start_date=2015-7-20&reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        
        response = self.client.get("/api/v1/meal/?end_date=2015-7-19")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        response = self.client.get("/api/v1/meal/?end_date=2015-7-19&reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        
        response = self.client.get("/api/v1/meal/?start_date=2015-7-20&end_date=2015-7-21")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)
        response = self.client.get("/api/v1/meal/?start_date=2015-7-20&end_date=2015-7-21&reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        
        response = self.client.get("/api/v1/meal/?start_date=2015-7-19&end_date=2015-7-20&end_time=12:00")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        response = self.client.get("/api/v1/meal/?start_date=2015-7-19&end_date=2015-7-20&end_time=12:00&reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        
        ## put
        response = self.client.put("/api/v1/meal/2/", '{"description": "meal2", "calories": 200, "date": "2015-7-20", "time": "11:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.put("/api/v1/meal/7/", '{"description": "meal2", "calories": 200, "date": "2015-7-18", "time": "6:30"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/api/v1/meal/?start_date=2015-7-19&end_date=2015-7-20&end_time=12:00")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        response = self.client.get("/api/v1/meal/?start_date=2015-7-19&end_date=2015-7-20&end_time=12:00&reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        
        ## delete
        response = self.client.delete("/api/v1/meal/2/")
        self.assertEqual(response.status_code, 204)
        response = self.client.delete("/api/v1/meal/7/")
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get("/api/v1/meal/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        response = self.client.get("/api/v1/meal/?reporter=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
