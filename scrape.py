from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests 
import os


# سرچ کردن ماشین در سایت و لینک صفحات
def Car (type) :
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    search_box.send_keys(type)
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(15)
    search_link = driver.find_elements(By.XPATH, "//a[contains(@class, 'kt-post-card__action')][@href]")
    return search_link

# فیلتر کردن صفحات دقیق شامل کلمه ماشین
def Linking (search_link , type):
    links = []
    link_main = []
    for link in search_link:
        links.append(link.get_attribute("href"))
    for head in links:
        driver.get(head)
        try:
            h1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            if type in h1.text:
                link_main.append(head)
        except Exception as e:
            print(f"Error accessing {head}: {e}")
    return link_main

# لینک عکس های تمامی صفحات به صورت لیست برای یک ماشین
def Imaging(link_main):
    image_links = []
    for ln in link_main:
        driver.get(ln)
        time.sleep(5)  # اضافه کردن خواب برای اطمینان از بارگذاری تصاویر
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        s1 = soup.findAll('div', {'class': 'kt-base-carousel__image'})
        for div in s1:
            img_tag = div.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_links.append(img_tag['src'])
    return image_links


# ذخیره عکس ها در پوشه مربوط به اسم همان خودرو
def file_save(image_ , type) :
    main_path = 'e:\\تحلیل داده\\challenge'
    os.chdir(main_path)
    main_file = 'dataset'
    car = type
    parent_path = os.path.join(main_path,main_file)

    if not os.path.exists(parent_path):
        os.mkdir(parent_path)

    car_dir = os.path.join(parent_path, car)

    if not os.path.exists(car_dir):
        os.mkdir(car_dir)


    for link in image_:
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(link , headers=headers , timeout= 10)
        
        total_files = len(os.listdir(car_dir))
        
        image_number = total_files + 1
        file_name = os.path.join(car_dir, f'image_{image_number}.jpg')
        
        with open(file_name, 'wb') as file:
            file.write(response.content)
        
car_ = ['پراید', 'سمند سورن', 'دنا' , 'پژو 405' , 'پژو 504' , 'سمند LX' , 'تارا' , 'رانا' , 'L90' , '206 SD V8' ]

for type in car_ :
    driver = webdriver.Chrome()
    driver.get("https://divar.ir/s/tehran")
    search_link = Car(type)
    link_ = Linking(search_link , type)
    image_ = Imaging(link_)
    file_save(image_ , type)

    print(f"Found {len(image_)} images for {type}.")
    driver.quit()

data_old = ['پراید', 'سمند سورن', 'دنا' , 'پژو 405' , 'پژو 504' , 'سمند LX' , 'تارا' , 'رانا' , 'L90' , '206 SD V8' ]
data_new = ['Peride', 'Samand_Soren', 'Dena' , '405' , '504' , 'Samand_LX' , 'Tara' , 'Rana' , 'L90' , '206_SD']

# مسیر پایه
base_path = r"e:\تحلیل داده\challenge\dataset"

for i in range(len(data_old)):
    # ساخت مسیر قدیمی و جدید با استفاده از مسیر پایه
    old_name = os.path.join(base_path, data_old[i])
    new_name = os.path.join(base_path, data_new[i])
    
    # بررسی وجود مسیر قبل از تغییر نام
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"پوشه '{data_old[i]}' با موفقیت به '{data_new[i]}' تغییر نام داده شد.")
    else:
        print(f"پوشه '{old_name}' وجود ندارد.")

print("تغییر نام تکمیل شد.")