import json
import requests

from .models import ConferenceVO


def get_conferences():
    url = "http://monolith:8000/api/conferences/"
    response = requests.get(url).json()
    # content = json.loads(response.content)
    for conference in response["conferences"]:
        ConferenceVO.objects.update_or_create(
            import_href=conference["href"],
            defaults={"name": conference["name"]},
        )
