import boto3

rekognition = boto3.client('rekognition')
a = rekognition.detect_moderation_labels(Image={'S3Object':{'Bucket':'rekogmatic-bucket','Name': 'groupon_img.jpg'}})
print a
