import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Ожидание кликабельнсти элемента
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    yield driver

    driver.quit()


MyPetsPage = 'https://petfriends.skillfactory.ru/my_pets'


class TestCardsMyPets:

    def test_show_my_pets(self, driver):
        driver.get(MyPetsPage)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="all_my_pets"]')))
        assert driver.find_element(By.TAG_NAME, 'h2').text == "LekSa"
        cards = driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        amount = statistics.text.split(': ')
        assert len(cards) == int(amount[1][0])
        print('Всего моих питомцев: ', int(amount[1][0]))

    def test_number_of_photos(self, driver):
        driver.get(MyPetsPage)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]/h2')))
        images = driver.find_elements(By.CSS_SELECTOR, 'img')
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        amount = statistics.text.split(': ')
        count = 0
        for i in range(len(images)):
            if images[i].get_attribute('src') != '':
                count += 1
        assert count > (int(amount[1][0]) // 2)

    def test_check_animal_data(self, driver):
        driver.get(MyPetsPage)
        driver.implicitly_wait(5)
        names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
        print(len(names))
        for i in range(len(names)):
            parts = names[i].text.split(', ')
            print('Элемент в names: ', names[i].text.split(' '))
            assert len(parts[0]) > 0

    def test_check_name(self, driver):
        # Проверка уникальности имен питомцев
        driver.get(MyPetsPage)
        driver.implicitly_wait(5)
        names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
        pet_name = []
        for i in range(len(names)):
            parts = names[i].text.split(' ')
            pet_name.append(parts[0])
        for i in range(len(pet_name) - 1):
            for j in range(i + 1, len(pet_name)):
                assert pet_name[i] != pet_name[j]


    @pytest.mark.xfail #Тест не будет падать при несовпадении элементов
    def test_check_all_animals(self, driver):
        # Проверка карточек на уникальность
        driver.get(MyPetsPage)
        driver.implicitly_wait(5)
        descriptions = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets table tbody tr')
        animal_data = []
        for i in range(len(descriptions)):
            animal_data.append(descriptions[i].text.split(' '))
        for i in range(len(animal_data) - 1):
            for j in range(i + 1, len(animal_data)):
                assert animal_data[i][0] != animal_data[j][0]
                assert animal_data[i][1] != animal_data[j][1]
                assert animal_data[i][2] != animal_data[j][2]
