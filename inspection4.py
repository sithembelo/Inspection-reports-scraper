from playwright.sync_api import sync_playwright
import pickle

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://aphis-efile.force.com/PublicSearchTool/s/inspection-reports')

        #inspect_button = page.query_selector('//*[@id="dynamoTab__item"]')
        inspect_button = page.wait_for_selector('//*[@id="dynamoTab__item"]', timeout=7000)
        inspect_button.click()

        search = page.wait_for_selector('//*[contains(concat( " ", @class, " " ), concat( " ", "slds-button_brand", " " ))]', timeout=5000)
        search.click()

        data_list = []
        next_ = page.wait_for_selector('//*[@id="dynamoTab"]/div[4]/div[3]/div/button', timeout=10000)
        for j in range(733):
            for i in range(1,101):
                data_dict  = {} 
                name_element = page.query_selector(f'//*[@id="dynamoTab"]/table/tbody/tr[{i}]/td[5]/div')
                data_dict['name'] = name_element.inner_text()

                cn = page.wait_for_selector(f'//*[@id="dynamoTab"]/table/tbody/tr[{i}]/td[2]/table/tr[1]/td[2]/div', timeout=10000)
                data_dict['customer_number'] = cn.inner_text()
            
                cert_num = page.query_selector(f'//*[@id="dynamoTab"]/table/tbody/tr[{i}]/td[2]/table/tr[2]/td[2]/div')
                data_dict['certificate_number'] = cert_num.inner_text()

                date_element = page.query_selector(f'//*[@id="dynamoTab"]/table/tbody/tr[{i}]/td[3]/div')
                data_dict['date'] = date_element.inner_text()

                url_ = page.query_selector(f'//*[@id="dynamoTab"]/table/tbody/tr[{i}]/td[1]/div/a')
                data_dict['url'] = url_.get_attribute('href')

                '''max_ = (page.query_selector('//*[@id="dynamoTab"]/div[3]/div[2]/div/b/text()[4]'))
                print(max_.inner_text())'''

                data_list.append(data_dict)

            print(data_list)
            with open('data.pkl', 'wb') as f:
                pickle.dump(data_list, f)
            next_.click()
            next_ = page.wait_for_selector('//*[@id="dynamoTab"]/div[4]/div[3]/div/button', timeout=20000)
            #page.wait_for_timeout(10000)
        
        browser.close()


if __name__ == '__main__':
    main()