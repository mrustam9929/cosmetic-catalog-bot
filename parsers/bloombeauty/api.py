import requests
from loguru import logger


class SiteAPI:
    CATEGORIES_URL = 'https://bloombeauty.uz/api/get-products'
    TOKEN = 'APA91bHEPwq4s0YX6ZuFyH5V9ESAghEajStg4KWtpdCDDvtg1d-CnySri864'
    PRODUCT_URL = "https://bloombeauty.uz/api/get-product"
    CATEGORY_PRODUCTS_URL = "https://bloombeauty.uz/api/get-main-products?category_id=63"
    BRANDS_URL = "https://bloombeauty.uz/api/get-brands"
    ALL_PRODUCTS_URL = 'https://bloombeauty.uz/api/get-products'

    def get_request_headers(self) -> dict:
        return {
            'Token': self.TOKEN
        }

    def get_categories(self) -> list:
        response = requests.get(self.CATEGORIES_URL, headers=self.get_request_headers())
        if response.status_code == 200:
            return response.json()['categories']
        logger.error(f"Ошибка парсинга {response.status_code} - {response.text}")
        return []

    def get_brands(self) -> list:
        response = requests.get(self.BRANDS_URL, headers=self.get_request_headers())
        if response.status_code == 200:
            return response.json()['data']
        logger.error(f"Ошибка парсинга {response.status_code} - {response.text}")
        return []

    def get_all_products(self):
        page = 1
        page_limit = 1

        while page <= page_limit:
            response = requests.post(
                url=self.ALL_PRODUCTS_URL,
                headers=self.get_request_headers(),
                data={
                    'page': page,
                    'pageSize': '20'
                })
            if response.status_code == 200:
                data = response.json()
                yield data['products']
                page += 1
                page_limit = data['pageCount']
            else:
                logger.error(f"Error {response.status_code}: {response.text}")
                break

    def get_product(self, url: str) -> dict:
        response = requests.get(self.PRODUCT_URL, headers=self.get_request_headers(), params={'url': url})
        if response.status_code == 200:
            return response.json()['product']
        logger.error(f"Ошибка парсинга {response.status_code} - {response.text}")
        return {}


api = SiteAPI()
