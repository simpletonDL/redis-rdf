import setuptools

setuptools.setup(
    name="cfpq_redis-simpletondl",
    version="0.0.4",
    author="Khoroshev and Terekhov",
    author_email="simpletondl@yandex.ru",
    description="Cfpq with python on RedisGraph",
    long_description="Cfpq with python on RedisGraph",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6'
)
