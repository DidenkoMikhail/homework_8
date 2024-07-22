import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация WebDriver
driver = webdriver.Chrome()

# URL страницы поиска вакансий
url = 'https://jobs.marksandspencer.com/job-search'

# Функция для парсинга вакансий
def scrape_jobs(page_url):
    driver.get(page_url)
    try:
        # Обновленный селектор для заголовков вакансий
        wait = WebDriverWait(driver, 10)
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ais-Hits-item')))
        job_list = []
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, '.text-2xl.bold.mb-16')
            link_element = job_element.find_element(By.CSS_SELECTOR, 'a.c-btn.c-btn--primary')
            title = title_element.text
            link = link_element.get_attribute('href')
            job_list.append({"title": title, "url": link})
        return job_list
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []

# Сбор данных с первых двух страниц
all_jobs = []
for page in range(1, 3):
    page_url = f'{url}?page={page}'
    print(f"Scraping page: {page_url}")
    all_jobs.extend(scrape_jobs(page_url))

# Сохранение данных в JSON файл
with open('jobs.json', 'w', encoding='utf-8') as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=4)

# Закрытие браузера
driver.quit()
