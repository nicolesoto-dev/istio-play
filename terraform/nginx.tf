resource "kubernetes_manifest" "nginx" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"

    metadata = {
      name      = "nginx"
      namespace = "argocd"
    }

    spec = {
      project = "default"

      source = {
        repoURL        = "https://github.com/YOUR_USER/YOUR_REPO.git"
        targetRevision = "main"
        path           = "apps/nginx"
      }

      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "nginx"
      }
    }
  }

  depends_on = [
    helm_release.argocd
  ]
}