import json
import boto3
import os
import psycopg2

def lambda_handler(event, context):
    try:
        v = 1.2
        bucket = event['Records'][0]['s3']['bucket']['name']
        filename  = event['Records'][0]['s3']['object']['key']
        
        rekognition = boto3.client('rekognition')
        #dynamodb = boto3.resource('dynamodb')

        j = rekognition.detect_moderation_labels(Image={'S3Object':{'Bucket':bucket,'Name': filename}})

        conn = psycopg2.connect("dbname='dbname' user='username' host='host' password='password'")
        cur = conn.cursor()
        cur.execute( "insert into image_moderation_tags values (  %s, %s,%s)", ( bucket, filename ,j['ModerationLabels']))
        conn.commit()
        cur.close()
        conn.close()
        #table = dynamodb.Table('image_metadata_w_tags')
        #response = table.put_item(
        #           Item={
        #                'image_name': bucket + '_' + filename,
        #                'moderation': json.dumps( j['ModerationLabels'])
        #            })
    except Exception as e:
        print e
        
    return 'Hello from Lambda'

