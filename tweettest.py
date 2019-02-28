"""Docstring."""
import requests
"""Docstring."""
fcurl = "https://services9.arcgis.com/sNLrO6i1xIbbnYSN/arcgis/rest/services/Tweets_Live_Stream/FeatureServer/0/applyEdits"    # NOQA

featurearray = [
    {
        "geometry": {
            "x": -110.28910,
            "y": 44.15542,
            "spatialReference": {
                "wkid": 4326
            }
        },
        "attributes": {
            "id": "11",
            "file": "Whatever we want here...",
            "time": "1537372090"
        }
    }
]

payload = {
    "token": "twitter token",   # Needs token, obviously
    "adds": featurearray,
    "f": "json"
}

headers = {
    'Content-Type': "application/x-www-form-urlencoded"
}

response = requests.request("POST", fcurl, data=payload, headers=headers)

print(response.text)
