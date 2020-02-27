import json


def create_lambda_event_dict():
    return json.loads('''\
    {
	"resource": "/admin/question",
	"path": "/admin/question",
	"httpMethod": "GET",
	"headers": {
		"Accept": "application/json",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
		"cache-control": "no-cache",
		"CloudFront-Forwarded-Proto": "https",
		"CloudFront-Is-Desktop-Viewer": "true",
		"CloudFront-Is-Mobile-Viewer": "false",
		"CloudFront-Is-SmartTV-Viewer": "false",
		"CloudFront-Is-Tablet-Viewer": "false",
		"CloudFront-Viewer-Country": "JP",
		"Host": "2mzeoft4ve.execute-api.ap-northeast-1.amazonaws.com",
		"origin": "http://localhost:8080",
		"pragma": "no-cache",
		"Referer": "http://localhost:8080/",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "cross-site",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
		"Via": "2.0 1dba622310b10f237c2fa77d70eb120f.cloudfront.net (CloudFront)",
		"X-Amz-Cf-Id": "OBGGbdzUzFF0h4Txw3TfwYS-ARgRKgx2PbZ_yi2ZXlI-JjCH0IeLPA==",
		"x-amz-date": "20200225T153207Z",
		"x-amz-security-token": "IQoJb3JpZ2luX2VjEMf//////////wEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAKJVZgztNqzFp0VLthpXfjwY05I57BDLzGkGL1tuDx25AiEAzpcbEF93AmGB1B3ZHtuSSvcpNmfKW/8r1hytFkGz7QUqpQQIkf//////////ARAAGgw2NjM0NTY1OTU3NzEiDD0ZGV5EIPPlH+EUVCr5A69KN5SSG/Q7a/6Tx8l2k7MstmpC6hcqVbKE7ykdZV8S5QW8a/jHR5Dd6EF1XtkLoNjlme9cXET5dFUjbF50qrfOtqv51H9lvRnM/Hed10IEAyT5YdDD5lk37UtvZeOon0HIjPS6OV6HNdiBZ/1zP5yTZT1x6qm9kQKa6UByJRKOxr8YVMzu1iGIoWzUvCRiSI3e625o/y5HnfMlVZIqDaYINvyBdRlOdzHFW8dsVcqalC3XcyqHhB6H6/zJCUsIRlUYXmZMXuR2ZMIXz3WP4Eoc37/Fifj7MPPUiq6RFAmyqylnru0NAezkdK3f0Lu4dGb8NSxGulRHH3aceLPvDV9n9ybMtBUUZyy9TH5WggCh7YlPSS5mMjFyXrXUje+9NziTOQDKF+2DMY9TpSShRDOc5H01VCVktmiISWF88y8z+JfovstUhkioOy1vKOOGtJWv2wHcIBS2pS+qZYbMlsevC0pBSsikKD0VKGDzBfXRre3v++By/D8jkh873tD4+o9wVrO5cjglGPA3L7KTTK6HpHgf6/sxxT6a03jYzSEZSyROobgkF1W3pKo0aJYgYdnlh4juJLEE/jvAvFjeqzKpmKRqXuuVw6OwT8/odvt5N7Au/XO0SeOX0iSsffFJZIosmENhwcO9UZCLXfypXN76dm6JlHqYKgAw9/vU8gU6ygJ+VdmDrI/G+X6hJhqxQe0zCPr/VTdBOqIZ3MAt/wx/mOJZ5PjYfJcGLSKKyJNSETQbnxomUEgqsej4AOlDEBFDGwSA5XtC9MOid/85mXtmTKaRnu73AnQNhaZiRNINGthaSx9FIk8mnOMr27aRx9JLv+g/CxjaN+nTKFl5ysipK+EoFV06Kq/wmHWVZhrjAd3b6PXh9D7N/rHnw3LTSePmcHzoh4JKq93GqhVVPfHojU0+7WeHpODf3I1Gc4DDxkSI9K6WzKeaNFNBGIMpKbJlZP3ApyKSzO3wIoE+eKzLd7w8ICFL9exSabeJzkXYKSBTu1IIuw93ZYiYQ8pmqrGctfG4u3Ez1prp1RgtGcmnk2/NSNfoB+TD+DM1tn247zSsCYngoWZmjJaDzCnoajWoc3zeaJv9pYNYaDn3tUXdFEizHmG2pkbkABY=",
		"X-Amzn-Trace-Id": "Root=1-5e553df7-3d72d8d8e93f0d00ef000aa8",
		"X-Forwarded-For": "115.124.242.86, 70.132.51.79",
		"X-Forwarded-Port": "443",
		"X-Forwarded-Proto": "https"
	},
	"multiValueHeaders": {
		"Accept": [
			"application/json"
		],
		"Accept-Encoding": [
			"gzip, deflate, br"
		],
		"Accept-Language": [
			"ja,en-US;q=0.9,en;q=0.8"
		],
		"cache-control": [
			"no-cache"
		],
		"CloudFront-Forwarded-Proto": [
			"https"
		],
		"CloudFront-Is-Desktop-Viewer": [
			"true"
		],
		"CloudFront-Is-Mobile-Viewer": [
			"false"
		],
		"CloudFront-Is-SmartTV-Viewer": [
			"false"
		],
		"CloudFront-Is-Tablet-Viewer": [
			"false"
		],
		"CloudFront-Viewer-Country": [
			"JP"
		],
		"Host": [
			"2mzeoft4ve.execute-api.ap-northeast-1.amazonaws.com"
		],
		"origin": [
			"http://localhost:8080"
		],
		"pragma": [
			"no-cache"
		],
		"Referer": [
			"http://localhost:8080/"
		],
		"sec-fetch-mode": [
			"cors"
		],
		"sec-fetch-site": [
			"cross-site"
		],
		"User-Agent": [
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
		],
		"Via": [
			"2.0 1dba622310b10f237c2fa77d70eb120f.cloudfront.net (CloudFront)"
		],
		"X-Amz-Cf-Id": [
			"OBGGbdzUzFF0h4Txw3TfwYS-ARgRKgx2PbZ_yi2ZXlI-JjCH0IeLPA=="
		],
		"x-amz-date": [
			"20200225T153207Z"
		],
		"x-amz-security-token": [
			"IQoJb3JpZ2luX2VjEMf//////////wEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAKJVZgztNqzFp0VLthpXfjwY05I57BDLzGkGL1tuDx25AiEAzpcbEF93AmGB1B3ZHtuSSvcpNmfKW/8r1hytFkGz7QUqpQQIkf//////////ARAAGgw2NjM0NTY1OTU3NzEiDD0ZGV5EIPPlH+EUVCr5A69KN5SSG/Q7a/6Tx8l2k7MstmpC6hcqVbKE7ykdZV8S5QW8a/jHR5Dd6EF1XtkLoNjlme9cXET5dFUjbF50qrfOtqv51H9lvRnM/Hed10IEAyT5YdDD5lk37UtvZeOon0HIjPS6OV6HNdiBZ/1zP5yTZT1x6qm9kQKa6UByJRKOxr8YVMzu1iGIoWzUvCRiSI3e625o/y5HnfMlVZIqDaYINvyBdRlOdzHFW8dsVcqalC3XcyqHhB6H6/zJCUsIRlUYXmZMXuR2ZMIXz3WP4Eoc37/Fifj7MPPUiq6RFAmyqylnru0NAezkdK3f0Lu4dGb8NSxGulRHH3aceLPvDV9n9ybMtBUUZyy9TH5WggCh7YlPSS5mMjFyXrXUje+9NziTOQDKF+2DMY9TpSShRDOc5H01VCVktmiISWF88y8z+JfovstUhkioOy1vKOOGtJWv2wHcIBS2pS+qZYbMlsevC0pBSsikKD0VKGDzBfXRre3v++By/D8jkh873tD4+o9wVrO5cjglGPA3L7KTTK6HpHgf6/sxxT6a03jYzSEZSyROobgkF1W3pKo0aJYgYdnlh4juJLEE/jvAvFjeqzKpmKRqXuuVw6OwT8/odvt5N7Au/XO0SeOX0iSsffFJZIosmENhwcO9UZCLXfypXN76dm6JlHqYKgAw9/vU8gU6ygJ+VdmDrI/G+X6hJhqxQe0zCPr/VTdBOqIZ3MAt/wx/mOJZ5PjYfJcGLSKKyJNSETQbnxomUEgqsej4AOlDEBFDGwSA5XtC9MOid/85mXtmTKaRnu73AnQNhaZiRNINGthaSx9FIk8mnOMr27aRx9JLv+g/CxjaN+nTKFl5ysipK+EoFV06Kq/wmHWVZhrjAd3b6PXh9D7N/rHnw3LTSePmcHzoh4JKq93GqhVVPfHojU0+7WeHpODf3I1Gc4DDxkSI9K6WzKeaNFNBGIMpKbJlZP3ApyKSzO3wIoE+eKzLd7w8ICFL9exSabeJzkXYKSBTu1IIuw93ZYiYQ8pmqrGctfG4u3Ez1prp1RgtGcmnk2/NSNfoB+TD+DM1tn247zSsCYngoWZmjJaDzCnoajWoc3zeaJv9pYNYaDn3tUXdFEizHmG2pkbkABY="
		],
		"X-Amzn-Trace-Id": [
			"Root=1-5e553df7-3d72d8d8e93f0d00ef000aa8"
		],
		"X-Forwarded-For": [
			"115.124.242.86, 70.132.51.79"
		],
		"X-Forwarded-Port": [
			"443"
		],
		"X-Forwarded-Proto": [
			"https"
		]
	},
	"queryStringParameters": null,
	"multiValueQueryStringParameters": null,
	"pathParameters": null,
	"stageVariables": null,
	"requestContext": {
		"resourceId": "5bgjku",
		"resourcePath": "/admin/question",
		"httpMethod": "GET",
		"extendedRequestId": "IdaesEYaNjMFv2Q=",
		"requestTime": "25/Feb/2020:15:32:07 +0000",
		"path": "/devmiyoshi/admin/question",
		"accountId": "663456595771",
		"protocol": "HTTP/1.1",
		"stage": "devmiyoshi",
		"domainPrefix": "2mzeoft4ve",
		"requestTimeEpoch": 1582644727568,
		"requestId": "95f21408-b05a-423c-a6c9-a3aeeacf578c",
		"identity": {
			"cognitoIdentityPoolId": "ap-northeast-1:06e7fa0c-c982-4e43-905f-dbb35de65387",
			"accountId": "663456595771",
			"cognitoIdentityId": "ap-northeast-1:a17abda7-e58d-4fdf-986b-81ba3cf981ab",
			"caller": "AROAZU6IYH456M7FT5ZGQ:CognitoIdentityCredentials",
			"sourceIp": "115.124.242.86",
			"principalOrgId": null,
			"accessKey": "ASIAZU6IYH45ZWV37QK7",
			"cognitoAuthenticationType": "authenticated",
			"cognitoAuthenticationProvider": "cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1G6B3pml2,cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1G6B3pml2:CognitoSignIn:79434f7e-b53f-4d3a-8c79-aedc7b73af39",
			"userArn": "arn:aws:sts::663456595771:assumed-role/toi-toy-authentication-devmiyos-ToiToyUserAuthRole-10G712RVDBAMA/CognitoIdentityCredentials",
			"userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
			"user": "AROAZU6IYH456M7FT5ZGQ:CognitoIdentityCredentials"
		},
		"domainName": "2mzeoft4ve.execute-api.ap-northeast-1.amazonaws.com",
		"apiId": "2mzeoft4ve"
	},
	"body": null,
	"isBase64Encoded": false
    }''')
