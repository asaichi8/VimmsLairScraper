import json
import time
from url_scraper import scrape_all_pages
from game_scraper import GameScraper


if __name__ == "__main__":
    pages = scrape_all_pages()

    rom_database = []
    count = 0
    start_time = time.time()
    file_name = "rom_database.json"

    gameScraper = GameScraper()
    for page in pages:
        for link in page:
            soup = gameScraper.scrape_html(link)
            info_table = gameScraper.extract_info_table(soup)

            title = gameScraper.extract_title(info_table)
            md5 = gameScraper.extract_md5_hash(info_table)

            if title:
                title = title.removesuffix(".nes")
            else:
                continue

            if not md5:
                continue

            rom_data = {
                "md5": md5,
                "name": title,
            }

            game_genie_table = gameScraper.extract_game_genie_table(soup)
            if game_genie_table:
                codes = gameScraper.extract_game_genie_codes(game_genie_table)

                if codes:
                    rom_data["game_genie_codes"] = [
                        {"code": code, "description": description} #, "is_active": False
                        for code, description in codes
                    ]

            count = count + 1
            rom_database.append(rom_data)

    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump({"roms": rom_database}, json_file, indent=4, ensure_ascii=False)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Wrote data for {count} ROMs to {file_name} in {elapsed_time:.1f} seconds.")
