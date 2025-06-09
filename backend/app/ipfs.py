import ipfshttpclient
from .config import settings

class IPFS_Client :

    def __init__ (self) :
        self.client = ipfshttpclient.connect(settings.IPFS_API_URL)
    
    def upload_file (self, file_bytes : bytes, file_name : str) -> str : 
        # return : ipfs에 업로드 한 후의 cid
        # paper 용
        res = self.client.add_bytes(file_bytes)
        return res
    
    def upload_text (self, text : str) -> str :
        # return : ipfs에 업로드 한 후의 cid
        # comment 용
        res = self.client.add_str(text)
        return res
    
    def get_file (self, ipfs_hash : str) -> bytes : 
        return self.client.cat(ipfs_hash)
    
    
ipfs_client = IPFS_Client()
