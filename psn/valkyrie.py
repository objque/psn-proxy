import requests


class ValkyrieAPIClient(object):
    def _get_discounts(self, usual, plus):
        discounts = []
        if usual["discount-percentage"] > 0 and not usual["is-plus"]:
            discounts.append({
                "is_plus": usual["is-plus"],
                "value": usual["actual-price"]["value"] / 100,
                "percentage": usual["discount-percentage"],
                "since": usual["availability"]["start-date"],
                "till": usual["availability"]["end-date"],
            })

        if plus["discount-percentage"] > 0 and plus["is-plus"]:
            discounts.append({
                "is_plus": plus["is-plus"],
                "value": plus["actual-price"]["value"] / 100,
                "percentage": plus["discount-percentage"],
                "since": plus["availability"]["start-date"],
                "till": plus["availability"]["end-date"],
            })
        return discounts

    def _get_actual_price_value(self, price):
        # game hasn't discount
        if not price["strikethrough-price"]:
            return price["actual-price"]["value"] / 100
        return price["strikethrough-price"]["value"] / 100

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
            "price": self._get_actual_price_value(price),
            "rate": {
                "total": included["attributes"]["star-rating"]["total"],
                "value": included["attributes"]["star-rating"]["score"],
            },
            "discounts": self._get_discounts(price, plus_price)
        }

    def resolve(self, id):
        base = "https://store.playstation.com/valkyrie-api"
        resp = requests.get(url=base + "/ru/RU/19/resolve/" + id, verify=False)
        return self._fix_resolve_answer(resp.json())
