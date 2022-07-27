data "aws_canonical_user_id" "current" {}


resource "aws_s3_bucket" "chats-json" {
  bucket                      = "chats-json"
  tags                        = {
        "Application" = "WhatsappAnalyzer"
      }
 tags_all                    = {
        "Application" = "WhatsappAnalyzer"
      }
}

