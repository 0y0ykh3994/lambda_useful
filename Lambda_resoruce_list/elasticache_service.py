class elasticache:
    def __init__(self, elasticache_service):
        self.elasticache_service = elasticache_service
        
    def describe_elasticache_info(self):
        response = self.elasticache_service.describe_cache_clusters()
        result_elasticache = []
    
        for cache_instances_info in (response['CacheClusters']):
            cache_cluster_id = cache_instances_info['CacheClusterId']
            cache_cluster_type = cache_instances_info['CacheNodeType']
            cache_cluster_engine = cache_instances_info['Engine']
            cache_cluster_engine_version = cache_instances_info['EngineVersion']
            cache_cluster_AZ = cache_instances_info['PreferredAvailabilityZone']
            
            result_elasticache.append((cache_cluster_id, cache_cluster_type, cache_cluster_engine, cache_cluster_engine_version, cache_cluster_AZ))
        return result_elasticache