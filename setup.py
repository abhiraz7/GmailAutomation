from setuptools import setup

setup(
    name="gmail-bot",
    version="1.0.0",
    py_modules=["gmail_bot"],
    install_requires=[
        "requests",
        "imapclient"
    ],
    entry_points={
        "console_scripts": [
            "gmail-bot = gmail_bot:main",
        ],
    },
)
