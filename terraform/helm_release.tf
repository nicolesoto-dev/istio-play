resource "helm_release" "argocd" {
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "10.18.0"

  name             = "argocd"
  namespace        = "argocd"
  create_namespace = true
}


# gitops-platform/
# │
# ├── terraform/
# │   ├── modules/
# │   │   ├── kind-cluster/
# │   │   ├── kubernetes-namespaces/
# │   │   ├── argocd-bootstrap/
# │   │   └── platform-resources/
# │   │
# │   ├── environments/
# │   │   ├── dev/
# │   │   └── production/
# │   │
# │   ├── providers.tf
# │   ├── versions.tf
# │   └── backend.tf
# │
# ├── argocd/
# │   ├── bootstrap/
# │   ├── projects/
# │   ├── applications/
# │   └── applicationsets/
# │
# ├── apps/
# │   ├── nginx/
# │   ├── monitoring/
# │   └── external-secrets/
# │
# ├── environments/
# │   ├── dev/
# │   ├── staging/
# │   └── production/
# │
# ├── helm/
# ├── kustomize/
# ├── policies/
# ├── observability/
# └── docs/