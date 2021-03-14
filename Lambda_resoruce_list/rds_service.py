class rds:
    def __init__(self, rds_service):
        self.rds_service = rds_service
        
    def get_param(self, rds_param_info):
        result = ''
        for rds_parameter_info in rds_param_info:
            result = rds_parameter_info.get('DBParameterGroups')
        return result
    
        
    def describe_rds_db_instances_info(self):
        response = self.rds_service.describe_db_instances()
        result_rds = []
        
        for db_instances in (response["DBInstances"]):
            db_instances_name = db_instances["DBInstanceIdentifier"]
            db_instances_address = db_instances["Endpoint"]["Address"]
            db_instances_port = str(db_instances["Endpoint"]["Port"]) + ' Port'
            db_instances_type = db_instances["DBInstanceClass"]
            db_instances_storage = str(db_instances["AllocatedStorage"]) + ' GiB'
            db_instances_engine = db_instances["Engine"]
            db_instances_engine_version = db_instances["EngineVersion"]
            db_instances_master_user = db_instances["MasterUsername"]
            db_instances_multi_az = db_instances["MultiAZ"]
            db_instances_availability_zone = db_instances["AvailabilityZone"]
            
            try:
                db_name = db_instances['DBName']
            except KeyError:
                db_name = ''
            
            result_rds.append((db_instances_name, db_name, db_instances_address, db_instances_port, db_instances_type, db_instances_storage, db_instances_engine, db_instances_engine_version, db_instances_master_user, db_instances_availability_zone, db_instances_multi_az))
        return result_rds
