terraform {
  backend "s3" {
    bucket = "arimo-infrastructure"
    key    = "terraform/infrastructure/pana-ap-jp-ccpm/main.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region  = var.region
  version = "~> 2.7"
}

provider "template" {
  version = "~> 2.1"
}

provider "null" {
  
}

module "ssh" {
  source = "github.com/adatao/DevOps//ops-ng/infrastructure/modules/ssh"
}
