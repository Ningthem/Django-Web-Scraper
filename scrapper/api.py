from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, JSONOpenAPIRenderer
from scrapper.models import Recipient, Slug, Product
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer
from datetime import datetime

# Scrapper
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from mailjet_rest import Client


class CheckApi(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONOpenAPIRenderer]

    def get(self, request):
        # num1 = request.data.get("num1")
        # user = User.objects.filter(id=5).first()

        # if num1 == 1:
        #     blog = Blog(title="API Title", content="API Content", user=user)
        #     blog.save()
        # num2 = request.data.get("num2")
        return Response({"message": 5}, )


class ScrapWeb(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONOpenAPIRenderer]

    def emailer(self, body, email, name):
        api_key = "ebfcb668f6a14de3fa0a9e3715159655"
        api_secret = "5e1b9a4cae9ca648661b7b553afd85da"
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {"Email": "neoyumnam@gmail.com", "Name": "Ningthem"},
                    "To": [{"Email": email, "Name": name}],
                    "Subject": "Important: Current prices",
                    "TextPart": "My first Mailjet email",
                    "HTMLPart": body,
            
                    "CustomID": "AppGettingStartedTest",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())

    def get(self, request):
        scrap_initialize_time = datetime.now()

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("window-size=1366x768")    # Very important

        web_url = "https://django-react-ecommerce.vercel.app/products/"

        slugs = Slug.objects.all()
        slug_list = list()

        for product in slugs:
            slug_list.append(product.slug)

        browser = webdriver.Chrome(
            executable_path=r"E:\Tutorials\Python\Web Scrapper\chromedriver.exe",
            options=options,
        )

        scrap_start_time = datetime.now()

        products_scrapped = dict()

        for slug in slug_list:
            browser.get(f"https://django-react-ecommerce.vercel.app/products/{slug}")

            price_xpath = '//*[@id="root"]/div[3]/div[2]/div/div/div[2]/div/div[1]/h3'
            product_name_xpath = ('//*[@id="root"]/div[3]/div[2]/div/div/div[2]/div/div[1]/h2')
            image_xpath = '//*[@id="root"]/div[3]/div[2]/div/div/div[1]/div/div[1]/img'

            try:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, price_xpath))
                )
                price_elem = browser.find_element_by_xpath(price_xpath).text[1:]
                name_elem = browser.find_element_by_xpath(product_name_xpath).text
                image_elem = browser.find_element_by_xpath(image_xpath).get_attribute(
                    "src"
                )
                products_scrapped[slug] = [slug, price_elem, image_elem, name_elem]
                # print(price_elem)
                # print(name_elem)

            except [TimeoutException, AttributeError, NameError]:
                print("Timeout")

        browser.quit()

        scrap_end_time = datetime.now()

        print(f'Start - Initialize : {(scrap_start_time - scrap_initialize_time).total_seconds()}')
        print(f'End - Start : {(scrap_end_time - scrap_start_time).total_seconds()}')
        print(f'Total Time: {(scrap_end_time - scrap_initialize_time).total_seconds()}')

        for name, item in products_scrapped.items():
            slug, latest_price, image_url, product_name = item[0], item[1], item[2], item[3]

            product = Product.objects.filter(slug=slug).first()
            if not product:
                new_product = Product(name=product_name, slug=slug, latest_price=latest_price, image_url=image_url, url=f'{web_url}{slug}')
                new_product.save()
            else:
                product.old_price = product.latest_price
                product.latest_price = latest_price
                product.save()

        all_products = Product.objects.all()
        email_body = ""
        diff_ind = 0
        for product in all_products:
            if(product.old_price > product.latest_price):
                email_body += f"""
                <h3>{product.name}</h3>
                <img src="{product.image_url}" width="200px" alt="">
                <br>
                <b>OldPrice: ${product.old_price}</b> <br>
                <b>New Price: ${product.latest_price}</b>
                <br>
                <b>Price dropped by ${product.old_price - product.latest_price}</b>
                <hr>
                """
                diff_ind = 1

        if diff_ind == 1:
            recipients = Recipient.objects.all()
            for person in recipients:
                self.emailer(body=email_body, email=person.email, name=person.email)
            print("Mail Sent")
        else:
            print("No Difference")
        return Response({"message": "Email Sent", "success_status": 1}, )


class ListProductAPI(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()