import re
import json
import emoji
import string
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Zemberek stop words eklemek için nltk'nin stopwordlerini ekleyin
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Türkçe stop words listesi, özel kelimeleri listeden çıkardık.
stop_words = set(stopwords.words("turkish"))
custom_stop_words = stop_words - {"değil", "ama"}  # Özel kelimeler çıkarıldı

# Emojiyi tespit eden bir yardımcı fonksiyon
def contains_emoji(text):
    return any(char for char in text if char in emoji.EMOJI_DATA)

# Metin ön işleme fonksiyonu
def preprocess_text(text):
    # Küçük harfe çevirme
    text = text.lower()
    # URL, kullanıcı adı (@kullanıcı) ve diğer gereksiz karakterleri kaldırma
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    # Noktalama işaretleri ve stop word'leri kaldırma
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in custom_stop_words]
    # Token'leri tekrar birleştirme
    return ' '.join(tokens)

# Model ve tokenizer yükleme
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
model = AutoModelForSequenceClassification.from_pretrained("dbmdz/bert-base-turkish-cased")
sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Duygu etiketlerini açıklama fonksiyonu
def map_label_to_sentiment(label):
    # Modelin verdiği etiketlere göre açıklama dönüştürme
    if label == 'LABEL_0':
        return 'NEGATIVE'
    elif label == 'LABEL_1':
        return 'POSITIVE'
    else:
        return 'NEUTRAL'

# JSON dosyasından duygu analizi yapmak için tweetleri okuma ve analiz fonksiyonu
def analyze_sentiments_from_json(json_file_path, output_json_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        tweets = json.load(f)

    processed_tweets = []

    for tweet in tweets:
        tweet_text = tweet.get("text", "")
        
        # Metni ön işleme tabi tutma
        preprocessed_text = preprocess_text(tweet_text)
        
        # Emojiyi kontrol etme
        emoji_exists = contains_emoji(tweet_text)
        
        # Duygu analizi yapma
        sentiment = sentiment_analysis(preprocessed_text)[0]
        
        # Duygu etiketini dönüştürme
        sentiment_label = map_label_to_sentiment(sentiment['label'])
        
        # İşlenmiş tweet verisini saklama
        processed_tweet = {
            "orijinal_text": tweet_text,
            "işlenmiş_text": preprocessed_text,
            "emoji_var": emoji_exists,
            "duygu": sentiment_label,
            "duygu_skala": sentiment['score']
        }
        processed_tweets.append(processed_tweet)

    # İşlenmiş tweetleri JSON dosyasına kaydet
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(processed_tweets, f, ensure_ascii=False, indent=4)
    
    return processed_tweets

# Analiz edilmiş sonuçları yazdırma
def print_analyzed_results(processed_tweets):
    for tweet in processed_tweets:
        print(f"Orijinal Tweet: {tweet['orijinal_text']}")
        print(f"İşlenmiş Tweet: {tweet['işlenmiş_text']}")
        print(f"Emoji Var: {tweet['emoji_var']}")
        print(f"Duygu: {tweet['duygu']}")
        print(f"Duygu Skala: {tweet['duygu_skala']}")
        print("=" * 50)

# Ana fonksiyon
def main():
    json_file_path = 'D:\Masaüstü\Istanbul_Sozlesmesi_Bitirme\İstanbul Sözleşmesi_2024-10-10_2024-10-11.json'  # Raw tweet verisi
    output_json_path = 'processed_tweets.json'  # İşlenmiş verinin kaydedileceği dosya

    processed_tweets = analyze_sentiments_from_json(json_file_path, output_json_path)
    print(f"{len(processed_tweets)} tweet işlendi ve kaydedildi: {output_json_path}")
    print_analyzed_results(processed_tweets)


if __name__ == "__main__":
    main()
