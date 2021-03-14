class iam:
    def __init__(self, iam_service):
        self.iam_service = iam_service
        
        
    def describe_iam_info(self):
        users = self.iam_service.list_users()
        result_iam = []
        
        alias_info = self.iam_service.list_account_aliases()
        alias = alias_info['AccountAliases']
        
        for iam_info in (users['Users']):
            
            arn = iam_info['Arn']
            arn_split = arn.split(':')
            account_num = arn_split[4]
            console_url = 'https://' + account_num + '.signin.aws.amazon.com/console'
            iam_user_name = iam_info['UserName']
            iam_user_id = iam_info['UserId']
            
            result_iam.append((iam_user_name, iam_user_id, alias, account_num, console_url))
        return result_iam