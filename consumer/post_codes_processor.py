class PostCodesProcessor:

    def __init__(self, post_codes: list) -> None:
        self.post_codes = post_codes
    
    def process_post_codes(self) -> list:
        
        post_codes = []
        for post_code in self.post_codes:
            
            if(post_code['result'] != None):
                post_codes.append(post_code)
            
        return post_codes
