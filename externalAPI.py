import requests


def fetch_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v3.6/product/{barcode}.json"
    headers = {"User-Agent": "MyApp/1.0(soma.enos@gmail.com)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") in (1, "success") and data.get("product"):
            return {"status": 1, "product": data.get("product", {})}
    except Exception as exc:
        print(f"product lookup failed: {exc}")

    fallback_url = f"https://world.openfoodfacts.net/api/v3.6/product/{barcode}.json"
    try:
        fallback_response = requests.get(fallback_url, headers=headers, timeout=10)
        fallback_response.raise_for_status()
        fallback_data = fallback_response.json()
        if fallback_data.get("status") in (1, "success") and fallback_data.get("product"):
            return {"status": 1, "product": fallback_data.get("product", {})}
    except Exception as exc:
        return {"status": 0, "error": str(exc)}

    return {"status": 0, "error": "Product not found"}


def fetch_by_name(name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }
    headers = {"User-Agent": "MyApp/1.0(soma.enos@gmail.com)"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        return {"products": products, "count": len(products)}
    except Exception as exc:
        return {"products": [], "count": 0, "error": str(exc)}




