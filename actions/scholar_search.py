from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScholarSearch:
    def __init__(self):
        self.driver = webdriver.Chrome()  # You can use any other webdriver here

    def search(self, query, limit=30, download=True):
        """
        Performs a query on scholar.google.com using Selenium, and returns a dictionary
        of results in the form {'papers': ...}. Unfortunately, as of now,
        captchas can potentially prevent searches after a certain limit.
        """
        SCHOLARS_BASE_URL = 'https://scholar.google.com'
        start = 0
        results = {'papers': []}

        self.driver.get(SCHOLARS_BASE_URL)
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'gs_r')))
                papers = self.driver.find_elements(By.CLASS_NAME, 'gs_r')
            except:
                results['err'] = f'Failed to complete search with query {query} (connection error)'
                self.driver.quit()
                return results

            if not papers:
                if 'CAPTCHA' in self.driver.page_source:
                    results['err'] = f'Failed to complete search with query {query} (captcha)'
                self.driver.quit()
                return results

            for paper in papers:
                pdf = None
                link = None

                try:
                    pdf = paper.find_element(By.CLASS_NAME, 'gs_ggs')
                except:
                    pass

                try:
                    link = paper.find_element(By.CLASS_NAME, 'gs_rt')
                except:
                    pass

                if pdf:
                    try:
                        source = pdf.find_element(
                            By.TAG_NAME, 'a').get_attribute('href')
                    except:
                        pass
                elif link:
                    try:
                        source = link.find_element(
                            By.TAG_NAME, 'a').get_attribute('href')
                    except:
                        pass
                else:
                    continue

                results['papers'].append({
                    'name': link.text if link else '',
                    'url': source
                })

                if len(results['papers']) >= limit:
                    self.driver.quit()
                    return results

            start += 10
            next_button = self.driver.find_element(By.ID, 'gs_n')
            if not next_button:
                self.driver.quit()
                return results
            next_button.click()


if __name__ == "__main__":
    scholar_search = ScholarSearch()
    search_results = scholar_search.search("MCDM", limit=30)
    print(search_results)
