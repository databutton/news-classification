import sys

sys.path.append(".")

import datetime

import databutton as db
import pandas as pd
import praw
import pycountry
from lib.config import DATA_KEY
from praw.models import Submission
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

reddit = praw.Reddit(
    client_id=db.secrets.get("REDDIT_CLIENT_ID"),
    client_secret=db.secrets.get("REDDIT_CLIENT_SECRET"),
    user_agent="news-classification",
    check_for_async=False,
)


def submissions(subreddit: str) -> Submission:
    for submission in reddit.subreddit(subreddit).new(limit=10):
        yield submission


def load_pipeline():
    # https://huggingface.co/ml6team/bert-base-uncased-city-country-ner
    tokenizer = AutoTokenizer.from_pretrained(
        "ml6team/bert-base-uncased-city-country-ner"
    )
    model = AutoModelForTokenClassification.from_pretrained(
        "ml6team/bert-base-uncased-city-country-ner"
    )

    return pipeline(
        "ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"
    )


def find_country(country: str):
    try:
        countries = pycountry.countries.search_fuzzy(country)
        if len(countries) == 0:
            print(f"Could not find country: {country}")
            return None
        elif len(countries) == 1:
            return countries[0]
        else:
            print(f"Found multiple countries for: {country}")
            return countries[0]
    except LookupError:
        print(f"Could not lookup: {country}")
        return None


@db.jobs.repeat_every(seconds=60, name="Fetch new posts from reddit")
def main(skip_id_check: bool = False):
    print("Fetching posts from reddit...")

    # Load existing dataset
    df = db.storage.dataframes.get(DATA_KEY)

    nlp = load_pipeline()

    scraped_at = datetime.datetime.now()
    for submission in submissions("worldnews"):
        if skip_id_check or not ("id" in df and df["id"] == submission.id).any():
            print(f"Processing post: {submission.title}")
            results = nlp(submission.title)
            for result in results:
                country = (
                    find_country(result["word"])
                    if result["entity_group"] == "COUNTRY"
                    else None
                )
                if country:
                    df = pd.concat(
                        [
                            df,
                            pd.DataFrame(
                                [
                                    {
                                        "id": submission.id,
                                        "title": submission.title,
                                        "country_name": country.name,
                                        "country_code": country.alpha_2,
                                        "country_flag": country.flag,
                                        "score": result["score"],
                                        "loc_start": result["start"],
                                        "loc_end": result["end"],
                                        "scraped_at": scraped_at,
                                        "url": f"https://redd.it/{submission.id}",
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

        else:
            print("Post already processed")

    # Save result
    df = db.storage.dataframes.put(df, DATA_KEY)


if __name__ == "__main__":
    main(skip_id_check=True)
