import os
import json
import csv

# JSON dosyalarının bulunduğu klasörün adı
json_folder = "json_files"  # Tüm JSON dosyalarınızı bu klasöre koyun
output_csv = "tweets.csv"  # Çıktı CSV dosyasının adı

# JSON dosyalarını listele
json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

# CSV dosyasını oluştur
with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Başlık satırını yaz
    header = ["tweet_id", "text", "username", "datetime", "tweet_link", "likes", "comments", "retweets", "photos", "hashtags"]
    csvwriter.writerow(header)
    
    # Tüm JSON dosyalarını birleştir ve veriyi CSV'ye yaz
    for file in json_files:
        file_path = os.path.join(json_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for tweet in data:
                csvwriter.writerow([
                    tweet.get("tweet_id", ""),
                    tweet.get("text", ""),
                    tweet.get("username", ""),
                    tweet.get("datetime", ""),
                    tweet.get("tweet_link", ""),
                    tweet.get("likes", ""),
                    tweet.get("comments", ""),
                    tweet.get("retweets", ""),
                    ";".join(tweet.get("photos", [])),
                    ";".join(tweet.get("hashtags", []))
                ])

print(f"Tüm JSON dosyaları birleştirildi ve '{output_csv}' adlı dosyaya kaydedildi!")
