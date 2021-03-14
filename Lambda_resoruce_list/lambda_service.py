class lambda_function:
    def __init__(self, lambda_function):
        self.lambda_function = lambda_function
        
    def describe_lambda_info(self):
        response = self.lambda_function.list_functions()
        result_lambda = []
        
        for lambda_info in (response['Functions']):
            lambda_function_name = lambda_info['FunctionName']
            lambda_function_runtime = lambda_info['Runtime']
            lambda_function_handler = lambda_info['Handler']
            
            result_lambda.append((lambda_function_name, lambda_function_runtime, lambda_function_handler,))
        return result_lambda
        
        