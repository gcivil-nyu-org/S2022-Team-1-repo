from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from posts.models import Post, Interest
from io import BytesIO
from PIL import Image
from django.core.files.base import File
import decimal


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.request_factory = RequestFactory()
        # self.client.login(username='testuser', password='12345')
        self.user = get_user_model().objects.create_user(
            username="user",
            password="12test12",
            email="user@nyu.edu",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admintestadmin",
            email="admin@nyu.edu",
        )
        self.poster = get_user_model().objects.create_user(
            username="test", password="12test12", email="test@example.com"
        )
        self.poster2 = get_user_model().objects.create_user(
            username="test2", password="12test12", email="test2@example.com"
        )
        self.poster3 = get_user_model().objects.create_user(
            username="different", password="12test12", email="test3@example.com"
        )

        # post2 = Post.objects.create(
        #     name="macbook pro",
        #     description="used macbook pro",
        #     option="exchange",
        #     category="tech",
        #     price=50,
        #     location="stern",
        #     user=self.poster,
        # )

    def test_admin_cannot_not_create_post(self):
        response = self.client.get("/posts/create/")
        self.assertEquals(response.status_code, 302)
        login = self.client.login(email="admin@nyu.edu", password="admintestadmin")
        self.assertEquals(login, True)
        response2 = self.client.get("/posts/create/")
        self.assertEquals(response2.status_code, 403)
        response3 = self.client.post("/posts/create/")
        self.assertEquals(response3.status_code, 403)

    def test_post_get(self):
        response = self.client.get("/posts/")
        self.assertEquals(response.status_code, 302)
        # login = self.client.force_login(self.user)
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response2 = self.client.get("/posts/")
        self.assertEquals(response2.status_code, 200)
        data = {"category": "tech", "option": "rent", "sort": "pricedesc"}
        response3 = self.client.get("/posts/", data)
        self.assertEquals(response3.status_code, 200)
        data2 = {"category": "tech", "option": "rent", "sort": "priceasc"}
        response4 = self.client.get("/posts/", data2)
        self.assertEquals(response4.status_code, 200)
        data3 = {"category": "tech", "option": "reported", "sort": "priceasc"}
        response5 = self.client.get("/posts/", data3)
        self.assertEquals(response5.status_code, 403)
        self.client.logout()
        self.assertEquals(login, True)
        login = self.client.login(email="admin@nyu.edu", password="admintestadmin")
        self.assertEquals(login, True)
        data4 = {"category": "tech", "option": "reported", "sort": "priceasc"}
        response6 = self.client.get("/posts/", data4)
        self.assertEquals(response6.status_code, 200)

    def test_post_create_get(self):
        response = self.client.get("/posts/create/")
        self.assertEquals(response.status_code, 302)
        # login = self.client.force_login(self.user)
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response2 = self.client.get("/posts/create/")
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, "posts/createpost.html")

    def test_detail_view(self):
        response = self.client.get("/posts/detail/1")
        self.assertEquals(response.status_code, 302)
        self.client.logout()
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response2 = self.client.get("/posts/detail/1")
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, "posts/detail.html")
        report = {"report": "report", "report_option": "4"}
        response3 = self.client.post("/posts/detail/1", report)
        self.assertEquals(response3.status_code, 302)
        cancel_report = {"cancel_report": "cancel_report"}
        response4 = self.client.post("/posts/detail/1", cancel_report)
        self.assertEquals(response4.status_code, 302)
        self.client.logout()
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        edit_denied = {"edit": "edit"}
        response9 = self.client.post("/posts/detail/1", edit_denied)
        self.assertEquals(response9.status_code, 403)
        interested = {"interested": "interested"}
        response5 = self.client.post("/posts/detail/1", interested)
        self.assertEquals(response5.status_code, 302)
        cancel_interested = {"cancel_interest": "cancel_interest"}
        response9 = self.client.post("/posts/detail/1", cancel_interested)
        self.assertEquals(response9.status_code, 302)
        self.client.logout()
        login = self.client.login(password="12test12", email="test@example.com")
        self.assertEquals(login, True)
        edit = {"edit": "edit"}
        response6 = self.client.post("/posts/detail/1", edit)
        self.assertEquals(response6.status_code, 403)
        delete = {"delete": "delete"}
        response7 = self.client.post("/posts/detail/1", delete)
        self.assertEquals(response7.status_code, 403)
        # response8 = self.client.get("/posts/detail/1")
        # self.assertEquals(response8.status_code, 404)

    def test_detail_view_admin(self):
        response = self.client.get("/posts/detail/1")
        self.assertEquals(response.status_code, 302)
        self.client.logout()
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        report = {"report": "report", "report_option": "4"}
        response1 = self.client.post("/posts/detail/1", report)
        self.assertEquals(response1.status_code, 302)
        self.client.logout()

        login = self.client.login(email="admin@nyu.edu", password="admintestadmin")
        self.assertEquals(login, True)
        response2 = self.client.get("/posts/detail/1")
        self.assertEquals(response2.status_code, 302)
        # self.assertEquals(len(response2.context["report_list"]), 1)
        self.client.logout()

        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        cancel_report = {"cancel_report": "cancel_report"}
        response3 = self.client.post("/posts/detail/1", cancel_report)
        self.assertEquals(response3.status_code, 302)
        self.client.logout()

        login = self.client.login(email="admin@nyu.edu", password="admintestadmin")
        self.assertEquals(login, True)
        response4 = self.client.get("/posts/detail/1")
        self.assertEquals(response4.status_code, 302)
        # self.assertEquals(response4.context["report_list"], None)
        self.client.logout()

    @staticmethod
    def get_image_file(name, ext="png", size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_create_post_edit_post(self):
        login = self.client.login(email="test@example.com", password="12test12")
        self.assertEquals(login, True)
        image1 = self.get_image_file("image.png")
        response = self.client.post(
            "/posts/create/",
            {
                "name": "macbook pro",
                "description": "used macbook pro",
                "option": "rent",
                "category": "tech",
                "price": 50,
                "location": "stern",
                "picture": image1,
            },
        )
        response2 = self.client.post(
            "/posts/create/",
            {
                "name": "macbook pro",
                "description": "used macbook pro",
                "option": "rent",
                "category": "tech",
                "price": 50,
                "location": "stern",
            },
        )
        response5 = self.client.post(
            "/posts/edit/1",
            {
                "name": "mac pro",
                "description": "used macbook pro",
                "option": "rent",
                "category": "tech",
                "price": 50,
                "location": "stern",
                "picture": image1,
            },
            pk=None,
            post_id=1,
        )
        self.assertEquals(response5.status_code, 200)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 200)
        post = Post.objects.get(id=1)
        self.assertEquals(post.user, self.poster)
        self.assertEquals(post.price, decimal.Decimal("50.00"))
        self.assertEquals(post.name, "macbook pro")
        self.assertEquals(post.description, "used macbook pro")
        self.assertEquals(post.location, "stern")
        response3 = self.client.get("/posts/edit/1", post_id=1)
        self.assertEquals(response3.status_code, 200)
        self.client.logout()
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response4 = self.client.get("/posts/edit/1", post_id=1)
        self.assertEquals(response4.status_code, 403)

    def test_interest_star(self):
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        post = Post.objects.get(id=1)
        post.interested_count += 1
        post.save()
        Interest.objects.create(
            post=post,
            interested_user=self.user,
            cust_message="interesting",
        )
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response = self.client.get("/posts/")
        self.assertEquals(response.status_code, 200)

    def test_query_title(self):
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        Post.objects.create(
            name="macb pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "macbook",
        }
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 1)
        self.assertEquals(response.status_code, 200)
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "macb",
        }
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 2)
        self.assertEquals(response.status_code, 200)

    def test_query_user(self):
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        Post.objects.create(
            name="macbooo",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        Post.objects.create(
            name="macb pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.user,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "test",
        }
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 2)
        self.assertEquals(response.status_code, 200)
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "user",
        }
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 1)
        self.assertEquals(response.status_code, 200)
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "noname",
        }
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 0)
        self.assertEquals(response.status_code, 200)
        Post.objects.create(
            name="item2",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster2,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        Post.objects.create(
            name="item3",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster3,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "test",
        }
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 2)
        self.assertEquals(response.status_code, 200)
        data = {
            "category": "tech",
            "option": "exchange",
            "sort": "time",
            "q": "dif",
        }
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 0)
        self.assertEquals(response.status_code, 200)
        # data = {
        #     "category": "tech",
        #     "option": "exchange",
        #     "sort": "time",
        #     "q": "",
        # }
        # response = self.client.get("/posts/", data)
        # self.assertIsNotNone(response.context["post_list"])
        # self.assertEquals(len(response.context["post_list"]), 1)
        # self.assertEquals(response.status_code, 200)

    def test_interest_option(self):
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        post = Post.objects.get(id=1)
        post.interested_count += 1
        post.save()
        Interest.objects.create(
            post=post,
            interested_user=self.user,
            cust_message="interesting",
        )
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        data = {"option": "interested"}
        response = self.client.get("/posts/", data)
        self.assertIsNotNone(response.context["post_list"])
        self.assertEquals(len(response.context["post_list"]), 1)
        Post.objects.create(
            name="macbook pro2",
            description="used macbook pro2",
            option="rent",
            category="tech",
            price=60,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        post2 = Post.objects.get(id=2)
        post.interested_count += 1
        post.save()
        Interest.objects.create(
            post=post2,
            interested_user=self.user,
            cust_message="fancy",
        )

        response2 = self.client.get("/posts/")
        self.assertEquals(response2.status_code, 200)
        data = {"option": "interested"}
        response3 = self.client.get("/posts/", data)
        self.assertIsNotNone(response3.context["post_list"])
        self.assertEquals(len(response3.context["post_list"]), 2)

    def test_post_delete(self):
        Post.objects.create(
            name="macbook pro",
            description="used macbook pro",
            option="exchange",
            category="tech",
            price=50,
            location="stern",
            user=self.poster,
            picture="https://nyu-marketplace-team1.s3.amazonaws.com/algo.jpg",
        )
        login = self.client.login(email="user@nyu.edu", password="12test12")
        self.assertEquals(login, True)
        response = self.client.get("/posts/detail/1")
        self.assertEquals(response.status_code, 200)
        post = Post.objects.get(pk=1)
        post.delete()
        response = self.client.get("/posts/detail/1")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/custom404.html")
