import sys
from scrapers.pitt_csc import scrape_pitt_csc
from scrapers.summer2027 import scrape_summer2027
from scrapers.offseason import scrape_offseason
from checkers.nvidia import check_nvidia
from checkers.google import check_google
from checkers.microsoft import check_microsoft
from checkers.meta import check_meta
from checkers.apple import check_apple
from checkers.amazon import check_amazon
from checkers.pinterest import check_pinterest
from checkers.duolingo import check_duolingo
from checkers.uber import check_uber
from checkers.stripe import check_stripe
from checkers.spotify import check_spotify
from checkers.dropbox import check_dropbox
from checkers.databricks import check_databricks
from checkers.palantir import check_palantir
from checkers.figma import check_figma
from checkers.snowflake import check_snowflake
from checkers.notion import check_notion
from checkers.datadog import check_datadog
from checkers.netflix import check_netflix
from checkers.salesforce import check_salesforce
from checkers.adobe import check_adobe
from checkers.intel import check_intel
from checkers.amd import check_amd
from checkers.qualcomm import check_qualcomm
from checkers.anthropic import check_anthropic
from checkers.openai import check_openai
from checkers.airbnb import check_airbnb
from checkers.mistral import check_mistral
from merge import merge_data, write_json


def main():
    bulk = []
    sources = [
        ("Summer 2026", scrape_pitt_csc, 'https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/master/README.md'),
        ("Summer 2027", scrape_summer2027, 'https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/main/README.md'),
        ("Off-Season", scrape_offseason, 'https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README-Off-Season.md'),
    ]
    
    for name, scraper, url in sources:
        try:
            entries = scraper(url)
            bulk.extend(entries)
            print(f'{name}: {len(entries)} entries')
        except Exception as e:
            print(f'{name} error: {e}', file=sys.stderr)

    top_tier = []
    for checker in [check_nvidia, check_google, check_microsoft, check_meta, check_apple, check_amazon, check_pinterest, check_duolingo, check_uber,
                    check_stripe, check_spotify, check_dropbox, check_databricks, check_palantir, check_figma, check_snowflake, check_notion, check_datadog,
                    check_netflix, check_salesforce, check_adobe, check_intel, check_amd, check_qualcomm, check_anthropic, check_openai, check_airbnb, check_mistral]:
        try:
            result = checker()
            if result:
                top_tier.append(result)
                print(f'{checker.__name__}: found entry')
        except Exception as e:
            print(f'{checker.__name__} error: {e}', file=sys.stderr)

    merged = merge_data(bulk, top_tier)
    write_json(merged, '../../data/internships.json')
    print(f'Wrote {len(merged)} total entries to data/internships.json')


if __name__ == "__main__":
    main()
