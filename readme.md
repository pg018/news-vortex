# NewsVortex

## Overview

NewsVortex is a Python application that allows you to summarize news articles based on user input. It utilizes various modules for fetching news, scraping content, and generating summaries.

Based on the query entered by user, the latest news articles are fetched, scrapped and thereafter summarized.

## Features

1. Summarize News Articles
2. Generate Training Data
3. Generate TF-IDF JSON

## Getting Started

### Prerequisites

1. Python 3.x
2. pip

### Installation

1. Clone the repository
2. Navigate to project directory
3. Install Dependencies => `pip install -r requirements.txt`
4. Setup environment variables
   1. Create a .env file in the project root by renaming the `.env.template` file
   2. Open the .env file and enter actual values for environment variables and remove the comments
5. Run the application through `main.py` in project root

## Reference

The data in `data` folder is currently on the following queries along with number of files related to it:

1. Elon Musk => 10
2. Narendra Modi => 6
3. Artificial Intelligence => 4
4. Recession => 1
5. India Stock Market => 7

The given sample TF-IDF JSON is also based on these queries...

The content in `result.json` is based on the query `rahul gandhi`
