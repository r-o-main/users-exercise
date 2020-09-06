from rest_framework.throttling import BaseThrottle
import ipapi


def get_originator_country_name_from(request):
    """ Use Django REST throttling to get the remote address
    See get_indet
    return country name
    """
    originator_ip_address = BaseThrottle().get_ident(request)
    try:
        originator_country = ipapi.location(ip=originator_ip_address, output='country_name')
        print(f"{originator_ip_address} is from {originator_country}")
        return originator_country.strip()
    except Exception as exc:
        print(f"[ipapi] Catched exception: {exc}")
        return None
