import datetime
from core.database import Base
from sqlalchemy import (
    JSON,
    DECIMAL,
    Index,
    Text,
    UniqueConstraint,
    func,
    text,
    Column,
    String,
    Integer,
    BigInteger,
    DateTime,
    Date,
    Boolean,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.mutable import MutableDict


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(String, index=True)
    session = Column(JSON, server_default="{}")
    name = Column(String, nullable=True)
    language = Column(String, server_default="ru")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=datetime.datetime.utcnow,
    )


class ProductBrand(Base):
    __tablename__ = "product_brands"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    slug = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)


class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    slug = Column(String, nullable=False, unique=True)
    name_ru = Column(String, nullable=True)
    name_en = Column(String, nullable=True)
    name_uz = Column(String, nullable=True)


class Site(Base):
    __tablename__ = "sites"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    category_id = Column(BigInteger, ForeignKey('product_categories.id', ondelete="SET NULL"), nullable=True)
    brand_id = Column(BigInteger, ForeignKey('product_brands.id', ondelete="SET NULL"), nullable=True)
    slug = Column(String, nullable=False, unique=True)
    name_ru = Column(String, nullable=True)
    name_en = Column(String, nullable=True)
    name_uz = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())


class SiteProduct(Base):
    __tablename__ = "site_products"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    site_id = Column(BigInteger, ForeignKey('sites.id', ondelete="CASCADE"))
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete="CASCADE"))
    category_id = Column(String, nullable=True)
    brand_id = Column(String, nullable=True)
    data = Column(JSON, server_default="{}")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    site = relationship("Site", backref="site_products")


class SiteProductHistory(Base):
    __tablename__ = "site_product_histories"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    site_product_id = Column(BigInteger, ForeignKey('site_products.id', ondelete="CASCADE"))
    price = Column(DECIMAL, server_default="0")
    discount = Column(DECIMAL, server_default="0")
    quantity = Column(DECIMAL, server_default="0")
    created_at = Column(DateTime, server_default=func.current_timestamp())
