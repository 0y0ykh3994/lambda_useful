import datetime

def lambda_handler(event, context):

     request = event['Records'][0]['cf']['request']
     headers = request['headers']

     langDirectoryList   = ["/kr", "/en", "/cn", "/tw", "/jp", "/kr/", "/en/", "/cn/", "/tw/", "/jp/"]
     hasDeviceCookie     = False # 디바이스 쿠키 존재 여부
     hasCountryDirectory = False # URL에 국가 주소 포함 여부
     viewerCountry       = headers.get('cloudfront-viewer-country')
     viewerMobile        = headers.get('cloudfront-is-mobile-viewer')
     viewerCallHost      = headers.get('host')[0]['value']
     deviceCookie        = 'NORMAL' # 기본은 PC로 이부분은 향후 논의 필요해 보임
     langDirectory       = ''
     queryString         = ''


    #print('request is {}'.format(request))

     #쿠키 확인
     for cookie in headers.get('cookie', []):
         if 'org.springframework.mobile.device.site.CookieSitePreferenceRepository.SITE_PREFERENCE' in cookie['value']:
             #print('Device cookie found')
             hasDeviceCookie=True
             break;

     #주소에 국가 코드가 존재 하는지 확인
     if  request['uri'] in langDirectoryList or request['uri'][0:4] in langDirectoryList:
         hasCountryDirectory=True

     #Device 쿠키도 존재하고 국가 코드 주소도 존재하면 Origin 으로 패스
     if hasDeviceCookie and hasCountryDirectory:
      #print('pass origin')
      return request

     #print('country value is {}'.format(viewerCountry))

     #리다이렉트 주소 변경
     if not hasCountryDirectory and viewerCountry: #국가 코드가 주소에는 없고 cloudfront-viewer-country는 헤더에 존재 할 경우
         countryCode = viewerCountry[0]['value']
         if countryCode == 'US':
             langDirectory = '/en'
         elif countryCode == 'JP':
             langDirectory = '/jp'
         elif countryCode == 'KR':
             langDirectory = '/kr'
         elif countryCode == 'TW':
             langDirectory = '/tw'
         elif countryCode == 'CN':
             langDirectory = '/cn'
         else:
             langDirectory = '/en'
     elif not hasCountryDirectory and not viewerCountry: #국가 코드가 주소에 없고 cloudfront-viewer-country또한 헤더에 존재 하지 않을 경우
         langDirectory = '/en'

     # 쿠키값 설정
     if not hasDeviceCookie and viewerMobile: # 디바이스 쿠키가 존재 하지않으나 cloudfront-is-mobile-viewer 헤더는 존재하는 경우
        isMobileCode = viewerMobile[0]['value']
        if isMobileCode == 'true':
            deviceCookie = "MOBILE"
        else:
            deviceCookie = "NORMAL"

     if request['querystring']: # query string 값이 있으면 추가
        queryString = '?'+request['querystring']


     response = {
         'status': '302',
         'statusDescription': 'Found',
         'headers': {
             'location': [{
                 'key': 'Location',
                 'value': 'https://'+viewerCallHost+langDirectory+request['uri']+queryString
             }],
         }
     }

     #쿠키 생성
     if not hasDeviceCookie:
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30) # expires in 30 days
        response['headers']['set-cookie'] = [{ 'key': "Set-Cookie", 'value': 'org.springframework.mobile.device.site.CookieSitePreferenceRepository.SITE_PREFERENCE='+deviceCookie +'; Path=/; Domain=mwave.me; Expires='+expires.strftime("%a, %d %b %Y %H:%M:%S GMT")}];


     #print("response is {}".format(response))

     return response
