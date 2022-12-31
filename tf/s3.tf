#####################################################
# S3 Bucket for data files
#####################################################
resource "aws_s3_bucket" "spotify_data_bucket" {
    bucket = var.data_bucket_name
}

# Bucket private access
resource "aws_s3_bucket_acl" "data_acl" {
    bucket = aws_s3_bucket.spotify_data_bucket.id
    acl    = var.acl_value
}

# Disable bucket public access
resource "aws_s3_bucket_public_access_block" "data_protected_bucket_access" {
    bucket = aws_s3_bucket.spotify_data_bucket.id

    # Block public access
    block_public_acls   = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

#####################################################
# S3 Bucket for lambda layer files
#####################################################
resource "aws_s3_bucket" "spotify_lambda_bucket" {
    bucket = var.lambda_bucket_name
}

# Bucket private access
resource "aws_s3_bucket_acl" "layer_acl" {
    bucket = aws_s3_bucket.spotify_lambda_bucket.id
    acl    = var.acl_value
}

# Disable bucket public access
resource "aws_s3_bucket_public_access_block" "layer_protected_bucket_access" {
    bucket = aws_s3_bucket.spotify_lambda_bucket.id

    # Block public access
    block_public_acls   = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

# Lambda layer files
resource "aws_s3_object" "s3_layer_requests" {
    bucket = aws_s3_bucket.spotify_lambda_bucket.id
    key    = "layer_requests.zip"
    source = "../deployment/layer_requests.zip"
    etag = filemd5("../deployment/layer_requests.zip")
}

resource "aws_s3_object" "s3_layer_spotipy" {
    bucket = aws_s3_bucket.spotify_lambda_bucket.id
    key    = "layer_spotipy.zip"
    source = "../deployment/layer_spotipy.zip"
    etag = filemd5("../deployment/layer_spotipy.zip")
}