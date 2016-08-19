from urllib.parse import urlparse
from scoremodel import app


class CSRFApi:
    def __init__(self, o_request):
        self.request = o_request
        self.base_url = urlparse(app.config['BASE_URL'])

    def origin(self):
        """
        OWASP Standard Header checks
        https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet#Standard_Header_Checks
        :return:
        """
        if self.request.headers.get('Origin'):
            origin = urlparse(self.request.headers.get('Origin'))
            if origin.scheme == self.base_url.scheme and origin.netloc == self.base_url.netloc:
                return True
        if self.request.headers.get('Referer'):
            referer = urlparse(self.request.headers.get('Referer'))
            if referer.scheme == self.base_url.scheme and referer.netloc == self.base_url.netloc:
                return True
        return False
