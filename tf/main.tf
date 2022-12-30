# create the lambda deployment package
data "archive_file" "deployment" {
  type        = "zip"
  source_file = "../scripts/get_album_lengths_from_playlist.py"
  output_path = "../deployment/get_album_lengths_from_playlist.zip"
}