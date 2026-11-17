terraform {
  required_version = ">=1.0"

  required_providers {

    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.9.1"
    }

    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "3.5.0"
    }

    helm = {
      source = "hashicorp/helm"
      version = "3.3.0"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "kind-cloudmart"
}

provider "helm" {
  kubernetes = {
    config_path = "~/.kube/config"
  }
}
