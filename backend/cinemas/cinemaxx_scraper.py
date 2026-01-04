import datetime
import os
from json import dumps

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from . import cinemaxx_locators
from .PreProcessors import movie_items, movie_information, movie_description, movie_timings
from ...ScrapingUtils import driver, utils

load_dotenv(verbose=True)


def run_cinemaxx_scraper(date, location):
    
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    
    target_url = os.environ.get('CINEMAXX_URL')

    if not target_url:
        raise ValueError("CINEMAXX url is not set")
    
    with driver.getdriver() as webdriver:
        webdriver.get(target_url)

        # webdriver = driver.getDriver(target_url)

        if utils.check_exists_by_xpath(webdriver, cinemaxx_locators.COOKIE_ACCEPT):
            webdriver.find_element(By.XPATH, cinemaxx_locators.COOKIE_ACCEPT).click()

            webdriver.find_element(By.XPATH, cinemaxx_locators.POP_UP).click()

        # webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        utils.web_driver_wait_visibility_of_element_by_xpath(webdriver, cinemaxx_locators.LOCATION.format(location))

        if utils.check_exists_by_xpath(webdriver, cinemaxx_locators.LOCATION.format(location)):
            webdriver.find_element(By.XPATH, cinemaxx_locators.LOCATION.format(location)).click()

        file_lists = ''
        movie_from_date = {}
        # utils.web_driver_wait_visibility_of_element_by_xpath(webdriver, cinemaxx_locators.FILM_LIST)

        if utils.check_exists_by_xpath(webdriver, cinemaxx_locators.FILM_LIST):
            file_lists = webdriver.find_elements(By.XPATH, cinemaxx_locators.FILM_CARDS)

        elif utils.check_exists_by_xpath(webdriver, cinemaxx_locators.NO_MOVIE):
            movie_from_date[date] = "Leider gibt es heute keine Filme, bitte wählen Sie einen anderen Termin"
            return movie_from_date

        movies = {}
        for i in range(1, len(file_lists) + 1):
            film_information = {}

            # Fetch all details related to picture, link and trailer
            film_information['movie_link'], film_information['movie_image_link'], film_information['trailer'] = \
                movie_items.get_movie_details(i, webdriver, cinemaxx_locators, utils)

            # Fetch Movie Information
            movie_info = movie_information.get_movie_information(webdriver, cinemaxx_locators, i)
            film_information['movie_title'] = movie_info[0]
            film_information['genres'] = movie_info[1]
            film_information['age_group'] = movie_info[2]
            film_information['movie_length'] = movie_info[3]

            # Fetch Movie Title
            film_information['synopsis'] = movie_description.get_movie_description(utils, webdriver, cinemaxx_locators, i)

            # Fetch Movie Timings
            film_information['movie_timings'] = movie_timings.get_movie_timings(webdriver, utils, cinemaxx_locators, i)

            # Add each movie information based on Title
            movies[film_information['movie_title']] = film_information

        movie_from_date[date] = movies
        with_indent = dumps(movie_from_date, indent=4, ensure_ascii=False)
        print(with_indent)
        
        return with_indent
