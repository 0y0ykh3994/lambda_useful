class vpc:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        
    def describe_vpc_info(self):
        response = self.ec2_service.describe_vpcs()
        vpc_name = ''
        result_vpc = []
        
        for vpc_info in response["Vpcs"]:
            vpc_cidr = vpc_info["CidrBlock"]
            vpc_id = vpc_info["VpcId"]
            
            try:
                for vpc_tag in vpc_info['Tags']:
                    if vpc_tag['Key'] == 'Name':
                        vpc_name = vpc_tag['Value']
            except KeyError:
                vpc_name = ''
                
            
            result_vpc.append((vpc_name, vpc_id, vpc_cidr))
        return result_vpc
        

'''
            for vpc_name_info in vpc_info['Tags']:
                try:
                    if vpc_name_info['Key'] == 'Name':
                        vpc_name = vpc_name_info["Value"]
                except KeyError:
                    vpc_name = ''
'''