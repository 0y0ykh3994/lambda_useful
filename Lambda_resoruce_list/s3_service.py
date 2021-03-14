class s3s:
    def __init__(self, s3_service):
        self.s3_service = s3_service
        
    def describe_s3s(self):
        s3_name_list = self.s3_service.list_buckets()
        result = []
        region = 'ap-northeast-2'
        
        for s3_name_info in s3_name_list['Buckets']:
            bucket_name = s3_name_info['Name']
            life_name = ''
            life_class = ''
            life_move_date = ''
            life_delete_date = ''
            
            try:
                s3_ac_info = self.s3_service.get_bucket_policy(Bucket=s3_name_info['Name'])
            except:
                s3_ac_info = ''
            
            try:
                s3_life_info = self.s3_service.get_bucket_lifecycle(Bucket=s3_name_info['Name'])['Rules'][0]
                life_name = s3_life_info['ID']
                life_delete_date = str(s3_life_info['Expiration']['Days']) + '일 후 파기'
            except:
                s3_life_info = ''
                
            try:
                s3_transition_info = self.s3_service.get_bucket_lifecycle(Bucket=s3_name_info['Name'])['Rules'][0]
                life_class = s3_life_info['Transition']['StorageClass']
                life_move_datelife_delete_date = str(s3_life_info['Transition']['Days']) + '일 후 이동'
            except:
                s3_transition_info = ''
            
            result.append((bucket_name, region, life_name, life_class, life_move_date, life_delete_date))
        return result