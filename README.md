# Gmail Automation Bot

![Gmail Automation Bot](https://img.shields.io/badge/Gmail%20Automation-Bot-blue)

## Overview

The **Gmail Automation Bot** is a Python-based tool designed to automate tasks related to Gmail. It connects to your Gmail account, searches for specific emails based on a keyword, extracts links from the email content, generates new URLs based on the extracted links, and performs actions on those URLs. This bot is highly customizable and can be adapted to various use cases.

## Features

- **IMAP Email Connection**: Connects to Gmail and other popular email providers using IMAP.
- **Keyword-Based Email Search**: Searches for unread emails with subjects that match a specified keyword.
- **Link Extraction**: Extracts URLs from the email body.
- **URL Generation**: Generates new URLs based on extracted links and predefined query parameters.
- **Automated Actions**: Sends GET requests to the generated URLs and opens them in a web browser.
- **Logging**: Provides detailed logging for all actions performed by the bot.

## Prerequisites

- Python 3.9 or higher
- Gmail account with IMAP enabled
- Gmail app password (for enhanced security)

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/gmail-automation-bot.git
    cd gmail-automation-bot
    ```

2. **Run the Installation Script**:
    ```sh
    install_gmail_bot.bat
    ```

    This script will check for Python installation, install it if not found, and then install the required dependencies.

## Usage

### Command Line Interface

1. **Run the Bot**:
    ```sh
    python gmailbot.py --email your-email@gmail.com --password your-app-password --subject "YourKeywordHere"
    ```

    Replace `your-email@gmail.com`, `your-app-password`, and `"YourKeywordHere"` with your actual email, app password, and the keyword you want to search for in email subjects.

### Continuous Execution

For continuous execution, use [gmailbotAll.py](http://_vscodecontentref_/0) which will keep checking for new emails every 2 seconds:

```sh
python gmailbotAll.py