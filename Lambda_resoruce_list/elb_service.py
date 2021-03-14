class elb:
    def __init__(self,elb_serivce):
        self.elb_serivce = elb_serivce
        
    def describe_elb_info(self):
        response = self.elb_serivce.describe_load_balancers()
        result_elb = []
        elb_type_info = 'classic'

        for elb_instances in (response["LoadBalancerDescriptions"]):
            elb_instances_name = elb_instances["LoadBalancerName"]
            elb_instances_endpoint = elb_instances["DNSName"]
            elb_instances_SG = elb_instances["SecurityGroups"]
            elb_instances_AZ = elb_instances["AvailabilityZones"]
            elb_instances_schem = elb_instances["Scheme"]
            elb_instance_type = elb_type_info
        
            result_elb.append((elb_instances_name, elb_type_info, elb_instances_schem, elb_instances_endpoint, elb_instances_AZ, elb_instances_SG))
        return result_elb