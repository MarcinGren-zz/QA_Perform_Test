#Website: http://www.performgroup.com/#our-divisions
#Check if all the hyperlinks for partnerships are active
#TODO export into .txt file

from selenium import webdriver
import os
import time
import config

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)

class PerformTest():

    def test(self):

        baseUrl = "http://www.performgroup.com/#our-divisions"
        driverLocation = config.chromeWebdriverLocation
        os.environ["webdriver.chrome.driver"] = driverLocation
        driver = webdriver.Chrome(executable_path=driverLocation, chrome_options=opts)
        driver.implicitly_wait(10)

        driver.get(baseUrl)
        driver.maximize_window()
        time.sleep(10)

        #Some hidden elements. Shows 16 in total but some are indexed as < 0 and they aren't shown because of that
        #11 elements in the list, 6 unique websites at the moment. These 6 getting shuffled when we use arrow.
        #Access img as we can distinguish the element from the others using it
        #then obtain href link that should be used as a parent - not every partnership might have it
        xpath = "//div[@class='business-carousel-wrapper']//div[contains(@class, 'slide slick-slide') and (@data-slick-index>='0')]"
        numberOfElements = len(driver.find_elements_by_xpath(xpath))
        print("Number of all partnership elements is: " + str(numberOfElements))

        #get unique names and their xpaths, then check if their parents 'a' have links
        listOfPartnershipNames = []
        listOfPartnershipXpaths = []
        for partners in list(range(numberOfElements)):
            partnerXpath = "(%s)[%s]//img" % (xpath, (partners + 1))
            partner = driver.find_element_by_xpath(partnerXpath)
            partnerAltAtr = str(partner.get_attribute("alt"))
            if partnerAltAtr not in listOfPartnershipNames:
                listOfPartnershipNames.append(partnerAltAtr)
                listOfPartnershipXpaths.append(partnerXpath)

        print("number of unique partnership names: " + str(len(listOfPartnershipNames)))
        #check parent links
        listOfPartnershipLinks = []
        for links in range(len(listOfPartnershipXpaths)):
            parentXpath = "%s//parent::a" % listOfPartnershipXpaths[links]
            try:
                partnershipLink = driver.find_element_by_xpath(parentXpath)
                if (partnershipLink.is_enabled()):
                    listOfPartnershipLinks.append(str(partnershipLink.get_attribute("href")))
            except:
                    print("failed while trying: " + listOfPartnershipNames[links])

        print(listOfPartnershipNames)
        print(listOfPartnershipXpaths)

chrome = PerformTest()
chrome.test()