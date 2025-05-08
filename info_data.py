import pandas as pd

# CSV dosyasını yükleyin
csv_file = "tweets.csv"  # CSV dosyanızın adı
df = pd.read_csv(csv_file)

# İlk birkaç satırı görüntüleyin
print("İlk 5 kayıt:")
print(df.head())

# Sütun isimlerini görüntüleyin
print("\nSütun isimleri:")
print(df.columns)

# Veri tipi ve eksik değer analizi
print("\nVeri türleri ve eksik değer sayıları:")
print(df.info())

# Temel istatistikler (sayısal veriler için)
print("\nTemel istatistikler:")
print(df.describe())
