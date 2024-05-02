def validate_github_url(url: str) -> None:
    """
    Validate if the url is based at GitHub or not,
    in case not it will raise ValueError.
    :param url: Url to validate
    :return: None
    """
    if not url or "https://" not in url:
        raise ValueError("Please, provide a valid url, such as https://...")
    if "github.com/" not in url:
        raise ValueError("Not supported VSC url, please add a GitHub url")
