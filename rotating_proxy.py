import requests
import random
import pycountry

def get_random_proxy():
    url = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all')
    list_proxies = url.text.split('\n')
    proxy = random.choice(list_proxies)
    print(f'Using proxy: {proxy}')

    # Get the IP address from the proxy (assuming it is in the format IP:PORT)
    ip_address = proxy.split(':')[0]

    # Make a request to ipinfo.io to get the country information
    ipinfo_url = f'http://ipinfo.io/{ip_address}/json'
    response = requests.get(ipinfo_url)
    if response.status_code == 200:
        ip_data = response.json()
        country_code = ip_data.get('country', 'Unknown')
        country_name = pycountry.countries.get(alpha_2=country_code).name
        print(f'The proxy is from {country_name}')
    else:
        print('Failed to fetch IP information.')

    return proxy

