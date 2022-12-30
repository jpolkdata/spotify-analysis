variable "AWS_ACCESS_KEY_ID" {
    type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
    type = string
}

variable "SPOTIPY_CLIENT_ID" {
  type = string
}

variable "SPOTIPY_CLIENT_SECRET" {
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