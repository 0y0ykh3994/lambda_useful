class elastictranscoder:
    def __init__(self, elastictranscoder_serivce):
        self.elastictranscoder_serivce = elastictranscoder_serivce
    
    def describe_elastictranscoder_info(self):
        response = self.elastictranscoder_serivce.list_presets()
        result_elastictranscoder = []
        
        
        
        print("===============elastictranscoder 정보===============")