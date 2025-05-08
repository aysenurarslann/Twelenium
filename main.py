import argparse
import datetime
from collector import Collector
from tweetDB import TweetDB

keywords = ['"İstanbul Sözleşmesi"']

search_query = " OR ".join(f'"{keyword}"' for keyword in keywords)

argv_parser = argparse.ArgumentParser()
argv_parser.add_argument('-s', '--start_date', type=str, required=True, help="Başlangıç tarihi YYYY-MM-DD")
argv_parser.add_argument('-e', '--end_date', type=str, required=True, help="Bitiş tarihi YYYY-MM-DD")
argv_parser.add_argument('-l', '--lang', type=str, default='tr', help="Tweet dili")
args = argv_parser.parse_args()

def main():
    start_date = args.start_date
    end_date = args.end_date
    lang = args.lang

    collector = Collector()
    db_conn = TweetDB(f"tweets_{start_date}_{end_date}")

    date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    date_end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    day = datetime.timedelta(days=1)

    target_dates = [date_start + datetime.timedelta(days=i) for i in range((date_end - date_start).days + 1)]

    missing_dates = []

    try:
        for date in target_dates:
            print(f"{date} için tweet'ler toplanıyor...")

            container = []
            collector.search(search_query, date, date + day, lang)
            collector.retrieve_tweets(container, keywords)

            if not container:
                print(f"Uyarı: {date} için toplanan tweet yok.")
                missing_dates.append(date)
                continue

            for tweet in container:
                db_conn.insert_tweet(tweet)

    except KeyboardInterrupt:
        print("\nTweet toplama işlemi kullanıcı tarafından durduruldu.")

    finally:
        if missing_dates:
            with open(f"missing_dates_{start_date}_{end_date}.txt", "w") as f:
                for missing_date in missing_dates:
                    f.write(f"{missing_date}\n")
            print(f"Eksik tarihler dosyaya yazıldı: missing_dates_{start_date}_{end_date}.txt")
        else:
            print("Hiç eksik tarih yok!")

        db_conn.export_to_json(f"tweets_{start_date}_{end_date}.json")
        print("Toplanan tüm tweet'ler:")
        db_conn.print_all_tweets()

        collector.close()
        db_conn.close()

if __name__ == "__main__":
    main()
