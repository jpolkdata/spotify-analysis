variable "aws_access_key" {
    type = string
}

variable "aws_secret_key" {
    type = string
}

variable "aws_region" {
    type    = string
    default = "us-east-1"
}

variable "bucket_name" {
    type    = string
    default = "spotify-analysis-jpolkdata"
}

variable "acl_value" {
    default = "private"
}