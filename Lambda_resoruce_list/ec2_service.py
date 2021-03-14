class ec2:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        
    def get_tag(self, ec2_tag_list):
        result = ''
        for ec2_info in ec2_tag_list:
            if ec2_info.get('Key') == 'Name':
                result = ec2_info.get('Value')
        return result

        
    def describe_ec2s(self):
        response = self.ec2_service.describe_instances()
        result_ec2 = []
                    
        for reservation in (response["Reservations"]):
            for instance in reservation["Instances"]:
                ec2_name = self.get_tag(instance.get('Tags'))
                ec2_id = instance["InstanceId"]
                ec2_type = instance["InstanceType"]
                ec2_place = instance["Placement"]["AvailabilityZone"]
                ec2_private_ip = instance["PrivateIpAddress"]
                
                result_ec2.append((ec2_name, ec2_id, ec2_type, ec2_private_ip, ec2_place))
        return result_ec2