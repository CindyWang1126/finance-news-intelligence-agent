resource "aws_s3_bucket" "digest_bucket" {
  bucket = "${var.project_name}-digest-bucket"
}
