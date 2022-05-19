from transformers import AutoModelForTokenClassification, AutoTokenizer


# Used to downlod a model to the /tmp-folder for offline mode
def main():
    modelIdentifier = "ml6team/bert-base-uncased-city-country-ner"
    tokenizer = AutoTokenizer.from_pretrained(modelIdentifier)
    model = AutoModelForTokenClassification.from_pretrained(modelIdentifier)

    tokenizer.save_pretrained("./tmp/{}".format(modelIdentifier))
    model.save_pretrained("./tmp/{}".format(modelIdentifier))


if __name__ == "__main__":
    main()
