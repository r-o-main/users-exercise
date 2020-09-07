from rest_framework.throttling import BaseThrottle
import ipapi


def get_originator_country_name_from(request):
    """ Get the originator country name for a given IP address from an HTTP request.
        Use Django REST throttling to get the remote address from the request
        and call the ipapi with it to retrieve the country name.
        Return the country name or "Undefined" if an exception occured during the call to ipapi
        (to mimic the response of ipapi).
    """
    originator_ip_address = BaseThrottle().get_ident(request)
    try:
        originator_country = ipapi.location(ip=originator_ip_address, output='country_name')
        print(f"{originator_ip_address} is from {originator_country}")
    except Exception as exc:
        print(f"[ipapi] Catched exception: {exc}")
        originator_country = "Undefined"
    return originator_country.strip()
