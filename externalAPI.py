import requests
# fetch Product by Barcode

def fetch_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v3.6/product/{barcode}.json"
    headers = {"User-Agent": "MyApp/1.0(soma.enos@gmail.com)"}

    try:
        response = requests.get(url, auth=("off","off"), headers=headers, timeout = 10)
        if response.status_code == 200:
            j = response.json()
            if j.get("status") == 1 or j.get("status") == "success":

                return {"status": 1, "product": j.get("product", {})}

    except Exception as e:
        print(f"product failed: {e}")
        
        
        fall_back = f"https://world.openfoodfacts.net/api/v3.6/product/{barcode}.json"

        res = requests.get(fall_back, headers=headers, timeout = 10)
        j = res.json()
        if j.get("status") == "success":
            return {"status": 1, "product":j.get("product", {})}
    except Exception as e:
        return{"status": 0, "error": str(e)}
    
    return{"status": 0, "error": "Product not Found"}

def fetch_by_name(name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_term": name,
        "json": True,
        "page_size": 5
    }
    headers = {"User-Agent": "MyApp/1.0(soma.enos@gmail.com)"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout= 10)
        return r.json()
    except Exception as e:
        return {"products": [], "error": str(e)}

# if __name__ == "__main__":
#     result = fetch_by_barcode("6111242100992")

#     if result["status"] == 1:
#         p = result["product"]
#         print("\n Suceeded")
#         print("name:", p.get("product_name"))
#         print("brands:", p.get("brands"))
#         print("Packaging:", p.get("packaging"))
#         print("Barcode:", p.get("barcode"))
#         # print(p)




