import requests


class ValkyrieAPIClient(object):
    def _fix_resolve_answer(self, json):
        included = json["included"][0]
        return {
            "id": included["id"],
            "type": included["type"],
            "name": included["attributes"]["name"],
            "release": included["attributes"]["release-date"],
            "poster": included["attributes"]["thumbnail-url-base"],
            "score": included["attributes"]["star-rating"],
            "prices": included["attributes"]["skus"][0]["prices"],
        }

    def resolve(self, id):
        base = "https://store.playstation.com/valkyrie-api"
        resp = requests.get(url=base + "/ru/RU/19/resolve/" + id, verify=False)
        return self._fix_resolve_answer(resp.json())
