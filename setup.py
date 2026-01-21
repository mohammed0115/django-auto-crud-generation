from setuptools import setup, find_packages

setup(
    name="django-auto-crud-generation",  # اسم الحزمة كما سيظهر على pip
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
        "djangorestframework>=3.14",
        "django-filter>=23.2",
        "pandas>=2.1",
        "openpyxl>=3.1",
        "python-decouple>=3.8",
        "xlrd>=2.0",
    ],
    entry_points={
        "console_scripts": [
            "manage=manage:main",
        ],
    },
    description="Automatic CRUD generation for Django models (Web + API + Templates + Exports + Permissions)",
    author="Your Name",
    url="https://github.com/mohammed0115/django-auto-crud-generation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
)
