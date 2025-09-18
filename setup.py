from setuptools import setup

from django_ent import __version__

setup(
    name="django-ent",
    version=__version__,
    description="Handle login and ticket validation for french ent (HDF, Occitanie, ...)",
    url="https://github.com/briefmnews/django-ent",
    author="Brief.me",
    author_email="tech@brief.me",
    license="MIT",
    packages=["django_ent", "django_ent.migrations"],
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.2",
        "python-cas>=1.6.0",
        "lxml>=4.9.4",
        "requests>=2.29.0",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    zip_safe=False,
)
