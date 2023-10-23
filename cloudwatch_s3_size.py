#!/usr/bin/env python3
# inspire by https://www.slsmk.com/getting-the-size-of-an-s3-bucket-using-boto3-for-aws/
import datetime
import locale
import boto3

locale.setlocale(locale.LC_ALL, 'nl_BE')

# For SSO, first set your profile in terminal else it uses default profile: aws sso login --profile profile-name
profile = 'profile-name'
boto3.setup_default_session(profile_name=profile)
client = boto3.client('cloudwatch')


def main(region='eu-west-1'):
    global item, sum_value
    now = datetime.datetime.now()
    cw = boto3.client('cloudwatch')
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S ")

    # Get a list of all buckets
    allbuckets = cw.list_metrics(Namespace='AWS/S3', MetricName='BucketSizeBytes')

    # Iterate through each bucket.
    for bucket in allbuckets['Metrics']:
        # For each bucket item, look up the corresponding metrics from CloudWatch.
        response = cw.get_metric_statistics(Namespace='AWS/S3',
                                            MetricName='BucketSizeBytes',
                                            Dimensions=bucket['Dimensions'],
                                            Statistics=['Sum'],
                                            Period=3600,
                                            StartTime=(now - datetime.timedelta(days=2)).isoformat(),
                                            EndTime=now.isoformat()
                                            )
        bucket_name = bucket['Dimensions'][1]['Value']
        # The cloudwatch metrics will have the single datapoint, so we just report on it.
        for item in response["Datapoints"]:
            sum_value = int(item["Sum"])
        formatted_sum = "{:n}".format(sum_value)

        # Check if the formatted string has more than 9 decimal places.
        if len(formatted_sum.split(",")[0]) > 9:
            print("{} {} {} {} GB".format(
                dt_string,
                region.ljust(14),
                bucket_name.ljust(45),
                formatted_sum[:-9].rjust(20)
            ))


if __name__ == '__main__':
    main()
