locals {
  glue_src_path = "${path.root}/../glue/"
}

variable "s3_bucket" {
  type=string
}

variable "project" {
  type=string
}