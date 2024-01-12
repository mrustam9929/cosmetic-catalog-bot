import pdb
from decimal import Decimal

from loguru import logger

from core.database import Session
from core.models import ProductBrand, ProductCategory, Site, SiteProduct, SiteProductHistory, Product
from parsers.bloombeauty.api import api
from slugify import slugify


def get_site(db: Session) -> Site:
    site = db.query(Site).where(Site.name == 'bloombeauty').one_or_none()
    if site is None:
        site = Site(name='bloombeauty', url='https://bloombeauty.uz')
        db.add(site)
        db.commit()
    return site


def get_discount(discount, old_price):
    old_price = Decimal(old_price)
    if old_price == Decimal(0):
        return old_price
    return Decimal(discount) / old_price * 100


def update_categories(site_categories: list, db: Session) -> dict:
    new_categories = []
    categories = {k: v for k, v in db.query(ProductCategory.slug, ProductCategory.id).all()}
    for site_category in site_categories:
        if site_category['url'] not in categories:
            new_categories.append(
                {
                    'name_ru': site_category['name_ru'],
                    'name_uz': site_category['name_uz'],
                    'name_en': site_category['name_en'],
                    'slug': slugify(site_category['name_ru'])
                }
            )
    db.bulk_insert_mappings(ProductCategory, new_categories)
    db.commit()
    return {k: v for k, v in db.query(ProductCategory.slug, ProductCategory.id).all()}


def update_brands(db: Session) -> dict:
    new_brands = []
    _brands = []
    brands = {k: v for k, v in db.query(ProductBrand.slug, ProductBrand.id).all()}
    for site_brand in api.get_brands():
        slug = slugify(site_brand['name'])
        if slug not in brands and slug not in _brands:
            new_brands.append({'name': site_brand['name'], 'slug': slug})
            _brands.append(slug)
    db.bulk_insert_mappings(ProductBrand, new_brands)
    db.commit()
    return {k: v for k, v in db.query(ProductBrand.slug, ProductBrand.id).all()}


def get_site_products(db: Session, site_id: int) -> dict:
    site_products = db.query(SiteProduct.product_id, SiteProduct.id).where(SiteProduct.site_id == site_id)
    return {k: v for k, v in site_products}


def start_parse_products():
    db = Session()
    site = get_site(db)
    brands = update_brands(db)
    site_products = get_site_products(db, site.id)
    product_histories = []
    for products_data in api.get_all_products():
        for product_data in products_data:
            try:
                if str(product_data['id']) in site_products:
                    site_product_id = site_products[product_data['id']]
                    price = Decimal(product_data['price'])
                    discount = get_discount(product_data['discount'], product_data['old_price'])
                    quantity = product_data['quantity']
                else:
                    slug = product_data['url']
                    product = db.query(Product).where(Product.slug == slug).one_or_none()
                    product_detail = api.get_product(slug)
                    if product is None:
                        brand_name = product_detail['brand_ru']
                        brand_id = brands.get(slugify(brand_name), None)
                        if brand_id is None:
                            brand = ProductBrand(slug=slugify(brand_name), name=brand_name)
                            db.add(brand)
                            db.commit()
                            brand_id = brand.id
                            brands[brand.slug] = brand_id
                        product = Product(
                            category_id=None,
                            brand_id=brand_id,
                            slug=slug,
                            name_ru=product_data['name_ru'],
                            name_uz=product_data['name_uz'],
                            name_en=product_data['name_en']
                        )
                        db.add(product)
                        db.commit()
                    site_product = SiteProduct(
                        site_id=site.id,
                        product_id=product.id,
                        category_id=product_detail['group_id'],
                        brand_id=product_detail['brand_id'],
                        data=product_detail
                    )
                    db.add(site_product)
                    db.commit()
                    site_product_id = site_product.id
                    price = Decimal(product_data['price'])
                    discount = get_discount(product_detail['discount'], product_detail['old_price'])
                    quantity = product_data['quantity']
                product_histories.append(
                    SiteProductHistory(
                        site_product_id=site_product_id,
                        price=price,
                        discount=discount,
                        quantity=quantity
                    )
                )
            except Exception as e:
                logger.error(str(e))
    db.bulk_insert_mappings(ProductBrand, product_histories)
    db.commit()
    db.close()
