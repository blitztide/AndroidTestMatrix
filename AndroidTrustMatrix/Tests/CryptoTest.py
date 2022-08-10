import ssl
from OpenSSL.crypto import load_certificate, FILETYPE_PEM

from AndroidTrustMatrix.Tests import BaseTest
class CryptoTest(BaseTest):
    def __init__(self,db):
        super()
        self.db = db
    def run(self,domain):
        certificate = self.get_certificate(domain)
        return 1
    
    def get_certificate(self,domain):
        context = ssl.create_default_context()
        certificate_der = ssl.get_server_certificate((domain,443))
        try:
            certificate = load_certificate(FILETYPE_PEM,certificate_der)
            fingerprint = certificate.digest("sha1")
            extensions = certificate.get_extension_count()
            for extension in range(extensions):
                data = certificate.get_extension(extension)
                if data.get_short_name() == b'certificatePolicies':
                    print(data)
            self.db.Add_Certificate(domain,certificate,fingerprint)
            return certificate
        except:
            return None
    
    def get_SSLVersion():
        return
