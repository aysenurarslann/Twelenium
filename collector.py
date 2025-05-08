#import json
import time
import re
#import pickle  # Çerezleri kaydedebilmek için pickle modülünü ekliyoruz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
class Collector:
    def __init__(self):
        # ChromeDriver servisini başlatıyoruz
        service = Service("D:\Masaüstü\chromedriver-win64\chromedriver.exe")
        options = Options()

        # Mevcut Chrome proflinizi kullanma
        user_profile_path ="C:\\Users\\Asus\\AppData\\Local\\Google\\Chrome\\User Data"
        options.add_argument(f"--user-data-dir={user_profile_path}")
        options.add_argument("--profile-directory=Profile 5")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
       
        # User-Agent bilgisi
        #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36")

        # Bot tespit edilmemesi için ayarlar
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Tarayıcıyı açık bırakmak için
        options.add_experimental_option("detach", True)

        # Tarayıcı başlatma
        self.driver = webdriver.Chrome(service=service, options=options)

    def search(self, search_key, from_, to_, lang='tr'):
        search_url = f"https://x.com/search?q={search_key}%20since%3A{from_}%20until%3A{to_}&lang={lang}&f=live"  # X.com arama URL'si
        self.driver.get(search_url)
        time.sleep(5)

    def retrieve_tweets(self, container, keywords=None):
        wait = WebDriverWait(self.driver, 20)

        # Sayfayı kaydırarak daha fazla tweet yüklenmesini sağla
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        max_attempts = 500  # Maksimum kaydırma deneme sayısı
        attempt = 0  # Şu anki deneme sayısı
        total_tweets = 0  # Toplam yüklenen tweet sayısı
        while attempt < max_attempts:
            try:
                # Space tuşu ile sayfayı kaydırma
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)

                # Sayfayı kaydırmadan önce bekleme
                time.sleep(7) 

                # Yeni yüklenen tweetleri yakala
                tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]')))
                if len(tweets) == total_tweets:
                    print("Yeni tweet yüklenmedi. Sayfa sonuna ulaşıldı.")
                    break
                total_tweets = len(tweets)
                for tweet in tweets:
                    try:
                        # Tweet metni ve hashtag'leri
                        tweet_text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                        hashtags = re.findall(r"#\\w+", tweet_text)

                        # Kullanıcı adı
                        username = tweet.find_element(By.XPATH, './/div[@dir="ltr"]//span[contains(text(), "@")]').text

                        # Tarih ve zaman
                        date_time = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')

                               # UTC -> Türkiye saati (UTC+3) dönüştürme
                        utc_datetime = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")  # ISO 8601 formatını datetime nesnesine çevir
                        turkey_datetime = utc_datetime + timedelta(hours=3)  # UTC+3 ekle

                        # Tweet ID ve bağlantısı
                        tweet_link = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute('href')
                        tweet_id = tweet_link.split("/")[-1]

                        # Sayac bilgileri
                        try:
                            comments_label = tweet.find_element(By.XPATH, './/button[@aria-label][contains(@aria-label, "Reply")]').get_attribute('aria-label')
                            comments = re.search(r'\d+', comments_label).group()  # Sadece sayıyı alır

                        except:
                            comments = '0'

                        try:
                            retweets_label = tweet.find_element(By.XPATH, './/button[@aria-label][contains(@aria-label, "Repost" )]').get_attribute('aria-label')
                            retweets = re.search(r'\d+', retweets_label).group()
                        except:
                            retweets = '0'

                        try:
                            likes_label = tweet.find_element( By.XPATH, './/button[@aria-label][contains(@aria-label, "Like" )]').get_attribute('aria-label')
                            likes = re.search(r'\d+', likes_label).group()
                        except:
                            likes = '0'

                        #try:
                            #views = tweet.find_element(By.XPATH, './/span[@data-testid="viewCount"]//span/span').text
                        #except:
                            #views = '0'

                        # Fotoğrafların URL'lerini alma
                        photos = tweet.find_elements(By.XPATH, './/img[@src]')
                        photo_urls = [photo.get_attribute('src') for photo in photos if 'profile_images' not in photo.get_attribute('src')]

                        # Her tweet için verileri sakla
                        container.append({
                            'text': tweet_text,
                            'username': username,
                            'datetime': turkey_datetime.strftime("%Y-%m-%d %H:%M:%S"),  # Türkiye saati
                            'tweet_id': tweet_id,
                            'tweet_link': tweet_link,
                            'likes': likes,
                            'comments': comments,
                            'retweets': retweets,
                            'photos': photo_urls,
                            #'views': views,
                            'hashtags': hashtags
                        })
                    except Exception as e:
                        print(f'Tweet verisi alınırken hata oluştu: {e}')

                # Sayfa sonuna kadar gelinmiş mi kontrol et
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            except Exception as e:
                print(f"Sayfa kaydırma sırasında hata oluştu: {e}")
                break
            finally:
                attempt += 1
        print(f"Toplam {len(container)} tweet toplandı.")    
    def close(self):
        self.driver.quit()

