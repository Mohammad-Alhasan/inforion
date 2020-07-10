def url_change(url):

    if url.find("ionapi") > 0:
        result = "https://mingle-sso.eu1.inforcloudsuite.com"

        return result
    else:
        return url
