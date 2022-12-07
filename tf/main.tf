provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region = "${var.aws_region}"
}

###############################
# Bucket creation
###############################
resource "aws_s3_bucket" "spotify_bucket" {
    bucket = "spotify-analysis-jpolkdata"
}

###############################
# Bucket private access
###############################
resource "aws_s3_bucket_acl" "example" {
    bucket = aws_s3_bucket.spotify_bucket.id
    acl    = "private"
}

###############################
# Disable bucket public access
###############################
resource "aws_s3_bucket_public_access_block" "protected_bucket_access" {
    bucket = aws_s3_bucket.spotify_bucket.id

    # Block public access
    block_public_acls   = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}