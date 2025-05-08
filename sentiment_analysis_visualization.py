import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import emoji

# Duygu analizi sonuçlarını içeren JSON dosyasını yükleme
def load_json_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Emojilerin olup olmadığını kontrol etme
def contains_emoji(text):
    return any(char for char in text if char in emoji.EMOJI_DATA)

# Duygu analizi skoru ve etiketi
# Duygu dağılımı grafiği
def plot_sentiment_distribution(processed_tweets):
    sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    
    for tweet in processed_tweets:
        sentiment = tweet.get("duygu", "NEUTRAL")  # Eğer 'duygu' yoksa varsayılan olarak 'NEUTRAL' al
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts["NEUTRAL"] += 1  # Bilinmeyen duygu varsa nötr olarak say

    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    
    # Grafiği oluşturma
    plt.figure(figsize=(8, 6))
    
    # 'labeldistance' ile etiketlerin mesafesini ayarlıyoruz
    # 'autopct' ile yüzde yazısını görselde düzenliyoruz
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, labeldistance=1.2,
            textprops={'size': 12, 'weight': 'bold', 'color': 'black'})
    
    plt.title('Duygu Dağılımı')
    plt.axis('equal')  # Daireyi yuvarlak yapmak için
    plt.show()


# Duygu skorlarını gösteren histogram
def plot_sentiment_scores(processed_tweets):
    sentiment_scores = [tweet.get('duygu_skala', 0) for tweet in processed_tweets]
    
    plt.figure(figsize=(8, 6))
    plt.hist(sentiment_scores, bins=20, color='#66b3ff', edgecolor='black', alpha=0.7)
    plt.title('Duygu Skorları Dağılımı')
    plt.xlabel('Duygu Skoru')
    plt.ylabel('Tweet Sayısı')
    plt.grid(True)
    plt.show()


# Kelime bulutu oluşturma
def plot_wordcloud(processed_tweets):
    # İşlenmiş metinleri al ve boş olanları filtrele
    text = " ".join([tweet.get('işlenmiş_text', '') for tweet in processed_tweets if tweet.get('işlenmiş_text')])
    
    if not text.strip():  # Eğer `text` boşsa uyarı ver ve devam et
        print("Kelime bulutu oluşturulamadı: Metin verisi yok.")
        return
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Kelime Bulutu')
    plt.show()

# Zaman içindeki duygu değişimi
def plot_sentiment_over_time(processed_tweets):
    tweet_dates = [tweet.get('datetime', '')[:10] for tweet in processed_tweets if 'datetime' in tweet]  # Sadece tarih kısmını al
    sentiment_scores = [tweet.get('duygu_skala', 0) for tweet in processed_tweets if 'datetime' in tweet]
    
    df = pd.DataFrame({'Date': tweet_dates, 'Sentiment Score': sentiment_scores})
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Tarih dönüşüm hatalarını 'NaT' olarak işaretle
    
    plt.figure(figsize=(10, 6))
    df.groupby('Date').mean()['Sentiment Score'].plot(kind='line', color='purple', marker='o')
    plt.title('Zaman İçindeki Duygu Skoru Değişimi')
    plt.xlabel('Tarih')
    plt.ylabel('Duygu Skoru')
    plt.grid(True)
    plt.show()

# Duygu durumunu kategorik olarak bar grafiği ile gösterme
def plot_sentiment_bar_chart(processed_tweets):
    sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    
    for tweet in processed_tweets:
        sentiment = tweet.get("duygu", "NEUTRAL")  # 'duygu' anahtarını güvenle al
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts["NEUTRAL"] += 1  # Bilinmeyen duygu varsa nötr olarak say

    plt.figure(figsize=(8, 6))
    plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['#66b3ff', '#ff9999', '#99ff99'])
    plt.title('Duygu Durumu (Pozitif, Negatif, Nötr)')
    plt.xlabel('Duygu')
    plt.ylabel('Tweet Sayısı')
    plt.grid(True)
    plt.show()

# Ana fonksiyon
def main():
    # JSON dosyasından veri yükleme
    json_file_path = 'D:\Masaüstü\Istanbul_Sozlesmesi_Bitirme\İstanbul Sözleşmesi_2024-10-10_2024-10-11.json'  # JSON dosyasının yolunu buraya yazın
    processed_tweets = load_json_data(json_file_path)
    
    # Duygu dağılımı grafiği
    plot_sentiment_distribution(processed_tweets)
    
    # Duygu skorları dağılımı histogramı
    plot_sentiment_scores(processed_tweets)
    
    # Kelime bulutu
    plot_wordcloud(processed_tweets)
    
    # Zaman içindeki duygu değişimi
    plot_sentiment_over_time(processed_tweets)
    
    # Duygu durumunu bar grafiği ile gösterme
    plot_sentiment_bar_chart(processed_tweets)

# Çalıştırma komutu
if __name__ == "__main__":
    main()
