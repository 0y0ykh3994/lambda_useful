class elbv2:
    def __init__(self, elbv2_service):
        self.elbv2_service = elbv2_service
        
    def get_az(self, elb_az_info):
        result = ''
        for elbv2_info in elb_az_info:
            result = elbv2_info.get('AvailabilityZones')
        return result
        
    
        
        
    def describe_elbv2_info(self):
        response = self.elbv2_service.describe_load_balancers()
        result_elbv2 = []
        az = ''
        ip_addr = ''
        security_g = ''
        
        for elbv2_instances in (response["LoadBalancers"]):
            elbv2_instances_name = elbv2_instances["LoadBalancerName"]
            elbv2_instances_type = elbv2_instances["Type"]
            elbv2_instances_schem = elbv2_instances["Scheme"]
            elbv2_instances_endpoint = elbv2_instances["DNSName"]
            
            
            try:
                security_g = elbv2_instances['SecurityGroups']
            except:
                security_g = 'None'
                
            try:
                for elbv2_az_info in elbv2_instances['AvailabilityZones']:
                    az += elbv2_az_info['ZoneName'] + ', '
            except:
                az = ''
    
            result_elbv2.append((elbv2_instances_name, elbv2_instances_type, elbv2_instances_schem, elbv2_instances_endpoint, security_g))
        return result_elbv2
        
'''
            for elbv2_az in elbv2_instances['AvailabilityZones']:
                az += elbv2_az["ZoneName"] + ', '
                
                for elbv2_ip in elbv2_az['LoadBalancerAddresses']:
                    try:
                        ip_addr += elbv2_ip['IpAddress'] + ', '
                    except:
                        ip_addr = 'None'
'''