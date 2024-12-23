import scraping_man_articles
import scraping_woman_aticles
import scraping_kids_articles

if __name__ == "__main__":
    print("Scraping men's products...")
    scraping_man_articles.main()

    print("Scraping women's products...")
    scraping_woman_aticles.main()

    print("Scraping kids' products...")
    scraping_kids_articles.main()