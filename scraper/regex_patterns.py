import re


class RegexPatterns:
    seller_name_regex = re.compile("Opinie o (.*)")
    number_of_reviews_regex = re.compile("([0-9]*).*")
    reputation_regex = re.compile(r"Ocena (.*) /")
    deliver_price_regex = re.compile("([0-9]+,[0-9]+)")

