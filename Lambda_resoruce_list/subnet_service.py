class subnet:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        
        
    def describe_subnet_info(self):
        response = self.ec2_service.describe_subnets()
        subnet_name = ''
        result_subnet = []
        
        for subnet_info in (response['Subnets']):
            subnet_cidr = subnet_info['CidrBlock']
            subnet_id = subnet_info['SubnetId']
            subnet_AZ = subnet_info['AvailabilityZone']
            
            try:
                for subnet_tag in subnet_info['Tags']:
                    if subnet_tag['Key'] == 'Name':
                        subnet_name = subnet_tag['Value']
            except:
                subnet_name = ''
            
            result_subnet.append((subnet_name, subnet_id, subnet_cidr, subnet_AZ))
        return result_subnet