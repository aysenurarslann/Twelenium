import json
from emotion_analysis import analyze_sentiments_from_json, print_analyzed_results

if __name__ == "__main__":
    # JSON dosyasının yolunu burada belirtin
    json_file_path = 'D:\Masaüstü\Istanbul_Sozlesmesi_Bitirme\İstanbul Sözleşmesi_2024-10-10_2024-10-11.json'  # Burada JSON dosyanızın tam yolunu kullanmalısınız.

    # Duygu analizini başlatma
    processed_tweets = analyze_sentiments_from_json(json_file_path)

    # Sonuçları yazdırma
    print_analyzed_results(processed_tweets)
