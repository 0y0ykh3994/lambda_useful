class igw:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        
    def get_tag(self, igw_tag_list):
        result = ''
        for igw_name_tag in igw_tag_list:
            if igw_name_tag.get('Key') == 'Name':
                result = igw_name_tag.get('Value')
            return result
            
    def get_attach_vpc(self, igw_vpc_list):
        result = ''
        for attach_vpc in igw_vpc_list:
            if attach_vpc.get('State') == 'available':
                result = attach_vpc.get('VpcId')
            return result
            
    def describe_igw_info(self):
        response = self.ec2_service.describe_internet_gateways()
        result_igw = []
        
        for igw_info in (response['InternetGateways']):
            igw_name = self.get_tag(igw_info.get('Tags'))
            igw_id = igw_info['InternetGatewayId']
            used_igw_vpc = self.get_attach_vpc(igw_info.get('Attachments'))
            
            result_igw.append((igw_name, igw_id, used_igw_vpc))
        return result_igw