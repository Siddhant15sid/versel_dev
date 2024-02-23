from django.test import TestCase, Client
from django.urls import reverse
from app.models import stock


class TestViews(TestCase):

    # def setUp(self):
    #     self.client=Client()
    #     self.get_news_url = reverse('get_news')
    #     self.login_url = reverse('index')
    #     self.index_url=reverse('index')
    #     self.get_news_url=reverse('get_news')


    def test_index_get(self):
        client=Client()
        response=client.get(reverse('index'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'login.html')

    def test_index_post(self):
        client=Client()
        response=client.post(reverse('index'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'homepage.html')

    # def test_get_news(self):
    #     login_data = {'email': 'siddhant@gmail.com', 'password': '1234'}
    #     self.client.post(self.login_url, data=login_data)

    #     # Access the get_news view
    #     response = self.client.post(self.get_news_url)

    #     # Check if the response status code is 200
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertEquals(response.status_code,200)

        # client=Client()
        # print(reverse('get_news'))
        # s1=stock.objects.get()
        # response=client.post(reverse('get_news'))
        # self.assertEquals(response.status_code,200)
        # self.assertTemplateUsed(response,'dashboard.html')