class nat:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
    
    def get_public_address(self, nat_address_list):
        result = ''
        for nat_address in nat_address_list:
            result = nat_address.get('PublicIp')
        return result
        
    def get_private_address(self, nat_address_list):
        result = ''
        for nat_address in nat_address_list:
            result = nat_address.get('PrivateIp')
        return result
        
    def describe_nat_info(self):
        response = self.ec2_service.describe_nat_gateways()
        result_nat = []
        nat_name = ''
        
        for nat_info in (response['NatGateways']):
            nat_id = nat_info['NatGatewayId']
            nat_public_ip = self.get_public_address(nat_info.get('NatGatewayAddresses'))
            nat_private_ip = self.get_private_address(nat_info.get('NatGatewayAddresses'))
            subnet_id = nat_info['SubnetId']
            
            try:
                for nat_name_tag in nat_info['Tags']:
                    if nat_name_tag['Key'] == 'Name':
                        nat_name = nat_name_tag['Value']
            except:
                nat_name = ''
                
            result_nat.append((nat_name, nat_id, nat_public_ip, nat_private_ip, subnet_id))
        return result_nat
        
'''
    def get_tag(self, nat_tag_list):
        result = ''
        for nat_name_tag in nat_tag_list:
            if nat_name_tag.get('Key') == 'Name':
                result = nat_name_tag.get('Value')
            return result
'''