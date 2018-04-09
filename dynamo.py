import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('image_metadata_w_tags')

a = table.get_item( Key={'image_name':'duggoo'})
print a
