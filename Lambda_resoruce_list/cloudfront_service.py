class cloudfront:
    def __init__(self, cloudfront_service):
        self.cloudfront_service = cloudfront_service

    def describe_cloudfront_info(self):
        response = self.cloudfront_service.list_distributions()
        result_cloudfront = []
        
        try:
            for cloudfront_info in response['DistributionList']['Items']:
                cloudfront_origin = ''
                cloudfront_cname = ''
                cloudfront_id = cloudfront_info['Id']
                cloudfront_domain = cloudfront_info['DomainName']
                for origin_info in cloudfront_info['Origins']['Items']:
                    cloudfront_origin += origin_info['DomainName']
                
                try:
                    for cloudfront_cname_info in cloudfront_info['Alias']['Items']:
                        cloudfront_cname += cloudfront_cname_info + ', '
                except KeyError:
                    cloudfront_cname = ''
                result_cloudfront.append((cloudfront_id, cloudfront_domain, cloudfront_origin, cloudfront_cname))
        except KeyError:
            result_cloudfront.append(('', '', '', ''))
            
        return result_cloudfront