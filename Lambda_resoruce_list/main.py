import boto3
import json
from boto3.session import Session
import s3_service, ec2_service, rds_service
import elb_service, elbv2_service, elasticache_service
import lambda_service, vpc_service, subnet_service
import igw_service, nat_service, cloudfront_service
import elasticsearch_service, elastictranscoder_service, iam_service
import concurrent.futures
import pandas as pd
import sys
from datetime import datetime

def get_iam_info(iam):
    iam = iam_service.iam(iam)
    
    get_iam_info = iam.describe_iam_info()
    return get_iam_info

def get_s3_info(s3):
    s3s = s3_service.s3s(s3)
    
    get_s3s_info = s3s.describe_s3s()
    return get_s3s_info
    
def get_ec2_info(ec2):
    ec2 = ec2_service.ec2(ec2)
    
    get_instances_info = ec2.describe_ec2s()
    return get_instances_info

def get_rds_info(rds):
    rds = rds_service.rds(rds)
    
    get_rds_db_instances_info = rds.describe_rds_db_instances_info()
    return get_rds_db_instances_info
    

def get_elb_info(elb):
    elb = elb_service.elb(elb)
    
    get_elb_instances_info = elb.describe_elb_info()
    return get_elb_instances_info


def get_elbv2_info(elbv2):
    elbv2 = elbv2_service.elbv2(elbv2)
    
    get_elbv2_instances_info = elbv2.describe_elbv2_info()
    return get_elbv2_instances_info
    
def get_elasticache_info(elasticache):
    elasticache = elasticache_service.elasticache(elasticache)
    
    get_elasticache_instances_info = elasticache.describe_elasticache_info()
    return get_elasticache_instances_info
    
def get_lambda_info(lambda_session):
    function = lambda_service.lambda_function(lambda_session)
    
    get_lambda_function = function.describe_lambda_info()
    return get_lambda_function
    
def get_vpc_info(vpc):
    vpc = vpc_service.vpc(vpc)
    
    get_vpc_info = vpc.describe_vpc_info()
    return get_vpc_info

def get_subnet_info(subnet):
    subnet = subnet_service.subnet(subnet)
    
    get_subnet_info = subnet.describe_subnet_info()
    return get_subnet_info

def get_igw_info(igw):
    igw = igw_service.igw(igw)
    
    get_igw_info = igw.describe_igw_info()
    return get_igw_info
    
def get_nat_info(nat):
    nat = nat_service.nat(nat)
    
    get_nat_info = nat.describe_nat_info()
    return get_nat_info
    
def get_cloudfront_info(cloudfront):
    cloudfront = cloudfront_service.cloudfront(cloudfront)
    
    get_cloudfront_info = cloudfront.describe_cloudfront_info()
    return get_cloudfront_info
    
def get_elasticsearch_info(elasticsearch):
    elasticsearch = elasticsearch_service.elasticsearch(elasticsearch)
    
    get_elasticsearch_info = elasticsearch.describe_elasticsearch_info()
    return get_elasticsearch_info
    
def get_elastictranscoder_info(elastictranscoder):
    elastictranscoder = elastictranscoder_service.elastictranscoder(elastictranscoder)
    
    get_elastictranscoder_info = elastictranscoder.describe_elastictranscoder_info()
    return get_elastictranscoder_info
    
    
    
def set_excel_info(first_type, label, value, sheet_name, n_sheet_name, excel_info, worksheet, start_row):
    workbook = excel_info.book
    # -----------------xlsx 디자인 용 -----------------------------
    # format to apply to xlsx
    all_format = workbook.add_format({
        'font_size': 10
    })
    # format to apply to xlsx
    border_format = workbook.add_format({
        'border': 1,
        'font_size': 10
    })
    # 최상위
    h_header_format = workbook.add_format({
        'bold': 1,
        'align': 'left',
        'font_size': 10
    })
    # 중앙정렬 format
    center_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'text_wrap': True
    })
    # 헤더 배경 + 글씨 format
    header_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'font_size': 10,
        'bg_color': '#9d9d9d'
    })
    # A라인 bold 처리
    bold_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })

    #-----------excel_set--------------
    df_info = pd.DataFrame.from_records(value, columns=label)
    df_info.index += 1
    df_info.to_excel(excel_info, sheet_name=sheet_name, startrow=start_row)
    if first_type:
        worksheet = excel_info.sheets[sheet_name]
        worksheet.write(0, 0, sheet_name, h_header_format)
    worksheet.write(start_row - 1, 0, n_sheet_name, h_header_format)
    worksheet.write(start_row, 0, '연번')

    st_row = start_row
    ed_row = st_row + len(df_info)

    # 포멧 설정
    # A라인 bold 처리
    worksheet.set_column('A:A', 18, bold_format)
    # 중앙 정렬
    worksheet.set_column('B:P', 18, center_format)
    # 헤더 색,배경
    worksheet.conditional_format(st_row, 0, st_row, len(label), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet.conditional_format(st_row, 0, ed_row, len(label), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    start_row += len(df_info) + 3

    return worksheet, start_row
    
def main(event, context):

    region = 'example.region'
    access_key = 'example.access_key'
    secret_key = 'example.secret_key'
    
    session = Session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    #s3 업로드 용
    s3_file_upload = boto3.client('s3')
    
    #service 가져오기
    iam = session.client('iam')
    ec2 = session.client('ec2')
    s3 = session.client('s3')
    rds = session.client('rds')
    elb = session.client('elb')
    elbv2 = session.client('elbv2')
    elasticache = session.client('elasticache')
    lambda_session = session.client('lambda')
    cloudfront = session.client('cloudfront')
    elasticsearch = session.client('es')
    elastictranscoder = session.client('elastictranscoder')
    
    xlsx_name = 'example.xlsx'
    
    
    write_resource = pd.ExcelWriter('/tmp/'+xlsx_name, engine='xlsxwriter')
    workbook = write_resource.book
    
    
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        t_iam = executor.submit(get_iam_info, iam)
        t_s3 = executor.submit(get_s3_info, s3)
        t_ec2 = executor.submit(get_ec2_info, ec2)
        t_rds = executor.submit(get_rds_info, rds)
        t_elb = executor.submit(get_elb_info, elb)
        t_elbv2 = executor.submit(get_elbv2_info, elbv2)
        t_elasticache = executor.submit(get_elasticache_info, elasticache)
        t_lambda = executor.submit(get_lambda_info, lambda_session)
        t_vpc = executor.submit(get_vpc_info, ec2)
        t_igw = executor.submit(get_igw_info, ec2)
        t_nat = executor.submit(get_nat_info, ec2)
        t_subnet = executor.submit(get_subnet_info, ec2)
        t_cloudfront = executor.submit(get_cloudfront_info, cloudfront)
        
        iam_values = t_iam.result()
        s3_values = t_s3.result()
        ec2_values = t_ec2.result()
        rds_values = t_rds.result()
        elb_values = t_elb.result()
        elbv2_values = t_elbv2.result()
        elasticache_values = t_elasticache.result()
        lambda_values = t_lambda.result()
        vpc_values = t_vpc.result()
        igw_values = t_igw.result()
        nat_values = t_nat.result()
        subnet_values = t_subnet.result()
        cloudfront_values = t_cloudfront.result()
    
    ec2_start_row = 3
    ec2_conn_labels = ['Instance Name', 'Instace Id', 'Instance Type', 'Private IP', 'EC2 Place']
    worksheet_ec2, dx_start_row = set_excel_info(True, ec2_conn_labels, ec2_values, '1.EC2', '1.1 EC2 자산현황', write_resource, '', ec2_start_row)
    
    rds_start_row = 3
    rds_conn_labels = ['RDB Name', 'DB Name', 'DNS Endpoint', 'Port', 'DB Instance Type', 'Storage', 'DB Engine', 'Engine Version', 'Admin user', 'RDS Place', 'Multi-AZ']
    worksheet_rds, dx_start_row = set_excel_info(True, rds_conn_labels, rds_values, '2.RDS', '2.1. RDS 자산현황', write_resource, '', rds_start_row)
    
    elb_start_row = 3
    elb_conn_labels = ['ELB Name', 'ELB Type', 'ELB Schme', 'DNS Endpoint', 'AvailabilityZones', 'SecurityGroups']
    worksheet_elb, dx_start_row = set_excel_info(True, elb_conn_labels, elb_values, '3.ELB', '3.1. CLB 자산현황', write_resource, '', elb_start_row)
    
    elbv2_start_row = 3
    elbv2_conn_labels = ['ELB Name', 'ELB Type', 'ELB Scheme', 'DNS Endpoint', 'SecurityGroups']
    worksheet_elbv2, dx_start_row = set_excel_info(True, elbv2_conn_labels, elbv2_values, '4.ELBV2', '4.1. NLB,ALB 자산현황', write_resource, '', elbv2_start_row)
    
    s3_start_row = 3
    s3_conn_labels = ['Bucket Name', 'Place', 'Life Cycle Name', 'Life Cycle Transition','Life Cycle Transition Days', 'Life Cycle Expiration Days']
    worksheet_s3, dx_start_row = set_excel_info(True, s3_conn_labels, s3_values, '5.S3', '5.1. S3 자산현황', write_resource, '', s3_start_row)
    
    vpc_start_row = 3
    vpc_conn_labels = ['VPC Name', 'VPC ID', 'VPC CIDR']
    worksheet_vpc, dx_start_row = set_excel_info(True, vpc_conn_labels, vpc_values, '6.VPC', '6.1 VPC 자산현황', write_resource, '', vpc_start_row)
    
    subnet_start_row = 3
    subnet_conn_labels = ['Subnet Name', 'Subnet ID', 'Subnet Cidr', 'Subnet Place']
    worksheet_subnet, dx_start_row = set_excel_info(True, subnet_conn_labels, subnet_values, '7.SUBNET', '7.1 Subnet 자산현황', write_resource, '', subnet_start_row)
    
    igw_start_row = 3
    igw_conn_labels = ['IGW Name', 'IGW ID', 'Attach VPC']
    worksheet_igw, dx_start_row = set_excel_info(True, igw_conn_labels, igw_values, '8.IGW', '8.1 IGW 자산현황', write_resource, '', igw_start_row)
    
    nat_start_row = 3
    nat_conn_labels = ['NAT Name', 'NAT ID', 'NAT Public IP', 'NAT Private IP', 'NAT Used Subnet']
    worksheet_nat, dx_start_row = set_excel_info(True, nat_conn_labels, nat_values, '9.NAT', '9.1 NAT 자산현황', write_resource, '', nat_start_row)
    
    elasticache_start_row = 3
    elasticache_conn_labels = ['Cluster Name', 'Cache Type', 'Redis Engine', 'Redis Version', 'AvailabilityZones']
    worksheet_elasticache, dx_start_row = set_excel_info(True, elasticache_conn_labels, elasticache_values, '10.Elasticache', '10.1. Elasticache 자산현황', write_resource, '', elasticache_start_row)
    
    cloudfront_start_row = 3
    cloudfront_conn_labels = ['Cloudfront Id', 'Cloudfront Domain', 'Cloudfront Origin', 'Cloudfront CNAME']
    worksheet_cloudfront, dx_start_row = set_excel_info(True, cloudfront_conn_labels, cloudfront_values, '11.Cloudfront', '11.1. Cloudfront 자산현황', write_resource, '', cloudfront_start_row)
    
    lambda_start_row = 3
    lambda_conn_labels = ['Function Name', 'Runtime Type & Version', 'Handler Name']
    worksheet_lambda, dx_start_row = set_excel_info(True, lambda_conn_labels, lambda_values, '12.Lambda', '12.1. Lambda 자산현황', write_resource, '', lambda_start_row)
    
    iam_start_row = 3
    iam_conn_labels = ['Console Account', 'Canonical User ID', 'Account Alias', 'Account Number', 'Console URL']
    worksheet_iam, dx_start_row = set_excel_info(True, iam_conn_labels, iam_values, '13.IAM', '13.1 AWS Account 자산현황', write_resource, '', iam_start_row)

    write_resource.save()
    
    bucket_name = 'example.bucket.name'
    s3_file_upload.upload_file('/tmp/'+xlsx_name, bucket_name, 'xlsx/'+xlsx_name)
    
    #function 실행
    get_iam_info(iam)
    get_ec2_info(ec2)
    get_s3_info(s3)
    get_rds_info(rds)
    get_elb_info(elb)
    get_elbv2_info(elbv2)
    get_elasticache_info(elasticache)
    get_lambda_info(lambda_session)
    get_vpc_info(ec2)
    get_subnet_info(ec2)
    get_igw_info(ec2)
    get_nat_info(ec2)
    get_elasticsearch_info(elasticsearch)

    status="complete"

    return status