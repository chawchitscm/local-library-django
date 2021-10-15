from django.http import JsonResponse, HttpResponse
import requests
from ip2geotools.databases.noncommercial import DbIpCity

class APIAdvertiserView():

    def track_visitor_ip(request):
        """
        api for tracking visitor ip address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        response = DbIpCity.get(ip, api_key='free')

        data = {
            'ip_adddress': response.ip_address,
            'city': response.city,
            'latitude': response.latitude,
            'longitude': response.longitude
            
        }
        return JsonResponse(data)

    def track_cookies(request):
        url = "https://httpbin.org/cookies"
        cookies = {'location': 'New York'}

        requestsJar = requests.cookies.RequestsCookieJar()
        requestsJar.set("browserId", "12345678", domain="httpbin.org", path="/cookies")

        r = requests.get(url, cookies=requestsJar)
        return HttpResponse(r.text)
        