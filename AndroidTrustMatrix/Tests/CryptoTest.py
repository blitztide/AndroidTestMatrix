import socket
from OpenSSL.crypto import dump_certificate, FILETYPE_ASN1
from OpenSSL import SSL
import re

from AndroidTrustMatrix.Tests import BaseTest
class CryptoTest(BaseTest):
    def __init__(self,db):
        super()
        self.db = db

    def run(self,domain):
        """Enumerate SSL for Domain"""
        Certificate = self.get_certificate(domain)
        Tcert = self.get_policy_score(Certificate)
        Ttls = self.get_SSL_Score(domain)
        Tssl = 5
        Tcrypto = (Tssl + Ttls + Tcert)/10
        return Tcrypto
    
    def get_certificate(self,domain):
        """Get SSL Server certificate presented to us"""
        # Create SSL context
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        #context.set_verify(SSL.VERIFY_PEER)
        # Create an SSL connection
        sock = socket.socket()
        SSL_Sock = SSL.Connection(context, sock)
        SSL_Sock.set_tlsext_host_name(domain.encode()) # SNI Support
        SSL_Sock.connect((domain,443))
        SSL_Sock.do_handshake()

        certificate = SSL_Sock.get_peer_certificate()
        sock.close()
        fingerprint = certificate.digest("sha1")
        raw_cert = dump_certificate(FILETYPE_ASN1,certificate)

        if not self.db.Get_Certificate(fingerprint):
            self.db.Add_Certificate(domain,raw_cert,fingerprint)
        self.db.Add_Certificate_Available(domain,fingerprint)
        
        return certificate
        
    def get_SSL_Score(self,domain):
         # Create SSL context
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        #context.set_verify(SSL.VERIFY_PEER)
        # Create an SSL connection
        sock = socket.socket()
        SSL_Sock = SSL.Connection(context, sock)
        SSL_Sock.set_tlsext_host_name(domain.encode()) # SNI Support
        SSL_Sock.connect((domain,443))
        SSL_Sock.do_handshake()
        version = SSL_Sock.get_protocol_version_name()
        Tssl = 0
        if not version == "Unknown":
            if version == "TLSv1.1":
                Tssl = 1
            if version == "TLSv1.2":
                Tssl = 1
            if version == "TLSv1.3":
                Tssl = 2
        sock.close()
        return Tssl
    
    def get_policy_score(self,Certificate):
        Tcert = 0
        extensions = Certificate.get_extension_count()
        for extension in range(extensions):
            data = Certificate.get_extension(extension)
            if data.get_short_name() == b'certificatePolicies':
                policy = re.findall("(2\.23\.140\.1\.2\.[1-3]|2\.23\.140\.1\.1)",data.__str__())
                if not policy == None:
                    if policy == "2.23.140.1.2.1": #Domain Validation
                        Tcert = 1
                    if policy == "2.23.140.1.2.2": # Organisational Validation
                        Tcert = 2
                    if policy == "2.23.140.1.2.3": # Individual Validation
                        Tcert = 2
                    if policy == "2.23.140.1.1": #Extended Validation
                        Tcert = 3
        return Tcert