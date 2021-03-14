class elasticsearch:
    def __init__(self, elasticsearch_service):
        self.elasticsearch_service = elasticsearch_service
        
    
    def describe_elasticsearch_info(self):
        response = self.elasticsearch_service.list_elasticsearch_instance_types(ElasticsearchVersion = '7.4')
        
        result_elasticsearch = [] 
        
        return result_elasticsearch