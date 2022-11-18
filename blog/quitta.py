import requests

class QuittaAPI :
  
  def get_django_artic(self):
    response = requests.get(
      "https://qiita.com/api/v2/tags/django/items"
    )
    
    json = response.json()
    print(json[0]['title'])