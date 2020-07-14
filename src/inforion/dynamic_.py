from urllib.parse import urlparse


def url_change(url):
    if "ionapi" in url:
        url = "https://mingle-sso.eu1.inforcloudsuite.com/BVB_DEV/"
        return url
    else:
        return url


url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/"
if "ionapi" in url:
    path = urlparse(url).path

    result = "https://mingle-sso.eu1.inforcloudsuite.com" + path
    print("Original: ", url)
    print("Extracted: ", result)
