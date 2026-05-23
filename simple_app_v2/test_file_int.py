"""
#API Testing: Framework Design a 
PyTest framework to test a REST API for traffic sign recognition. 
Create fixtures for API client, 
use Pandas to load test data, validate JSON response, 
and generate HTML report using Plotly.
"""

import pandas as pd
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

#data = pd.read_csv("file.csv")

# @pytest.fixture
# def test_api():
#     payload = data
#     response = requests.get(url, payload= payload)

#     return response


# def test_response(test_api):
#     response_data = test_api.json()

#     assert test_api.status_code() == 200
#     assert payload['signature'] == response_data['signature']


"""
Create a PyTest framework with Page Object Model (POM) f
or automating a Driver Monitoring System (DMS) web UI. 
Implement fixtures for Chrome/Firefox browser setup and teardown, 
use explicit waits for dynamic elements (camera feed, alerts), 
parametrize tests for different driver states (drowsy, distracted, normal), 
and capture screenshots on failure.

"""

# @pytest.fixture
# def test_url():
#     driver = webdriver.Chrome()
#     driver.get(url)


# project structure
# tests/
# --conftest.py
# --test_dms.py
# pages/
# --base_page.py
# --dms_page.py
# utils/
# --helpers.py