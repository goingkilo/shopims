#!/usr/bin/env ruby

require 'time'
require 'uri'
require 'openssl'
require 'base64'

# Your Access Key ID, as taken from the Your Account page
ACCESS_KEY_ID = "AKIAJTOAKS54QJPXPGIA"

# Your Secret Key corresponding to the above ID, as taken from the Your Account page
SECRET_KEY = "mFbVXMb0jm8HPdKVLVAzRwlr5F5zRivbS1fXd7dC"

# The region you are interested in
ENDPOINT = "webservices.amazon.in"

REQUEST_URI = "/onca/xml"

params = {
  "Service" => "AWSECommerceService",
  "Operation" => "ItemSearch",
  "AWSAccessKeyId" => "AKIAJTOAKS54QJPXPGIA",
  "AssociateTag" => "karthikraghun-21",
  "SearchIndex" => "Books",
  "Keywords" => "zen",
  "ResponseGroup" => "Images,ItemAttributes,Offers"
}

# Set current timestamp if not set
params["Timestamp"] = Time.now.gmtime.iso8601 if !params.key?("Timestamp")

# Generate the canonical query
canonical_query_string = params.sort.collect do |key, value|
  [URI.escape(key.to_s, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")), URI.escape(value.to_s, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"))].join('=')
end.join('&')

# Generate the string to be signed
string_to_sign = "GET\n#{ENDPOINT}\n#{REQUEST_URI}\n#{canonical_query_string}"

# Generate the signature required by the Product Advertising API
signature = Base64.encode64(OpenSSL::HMAC.digest(OpenSSL::Digest.new('sha256'), SECRET_KEY, string_to_sign)).strip()

# Generate the signed URL
request_url = "http://#{ENDPOINT}#{REQUEST_URI}?#{canonical_query_string}&Signature=#{URI.escape(signature, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"))}"

puts "Signed URL: \"#{request_url}\""

