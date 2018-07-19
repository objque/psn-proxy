import requests


class ValkyrieAPIClient(object):
    def _fix_resolve_answer(self, json):
        included = json["included"][0]
        price = included["attributes"]["skus"][0]["prices"]["non-plus-user"]
        plus_price = included["attributes"]["skus"][0]["prices"]["plus-user"]
        return {
            "id": included["id"],
            "name": included["attributes"]["name"],
            "poster": included["attributes"]["thumbnail-url-base"],
            "type": included["type"],
            "released": included["attributes"]["release-date"],
            "price": price["strikethrough-price"]["value"] / 100,
            "rate": {
                "total": included["attributes"]["star-rating"]["total"],
                "value": included["attributes"]["star-rating"]["score"],
            },
            "discounts": [
                {
                    "is_plus": price["is-plus"],
                    "value": price["actual-price"]["value"] / 100,
                    "percentage": price["discount-percentage"],
                    "since": price["availability"]["start-date"],
                    "till": price["availability"]["end-date"],
                },
                {
                    "is_plus": plus_price["is-plus"],
                    "value": plus_price["actual-price"]["value"] / 100,
                    "percentage": plus_price["discount-percentage"],
                    "since": plus_price["availability"]["start-date"],
                    "till": plus_price["availability"]["end-date"],
                },
            ]
        }

    def resolve(self, id):
        base = "https://store.playstation.com/valkyrie-api"
        resp = requests.get(url=base + "/ru/RU/19/resolve/" + id, verify=False)
        return self._fix_resolve_answer(resp.json())
