import models.com.example.platform.v1alpha1 as platformv1alpha1
import models.io.upbound.gcp.v1beta1 as gcpv1beta1
import models.io.upbound.dev.meta.v1alpha1 as metav1alpha1

_items = [
    metav1alpha1.E2ETest{
        metadata.name = "e2etest-xstoragebucket-kcl"
        spec = {
            crossplane.autoUpgrade.channel = "Rapid"
            defaultConditions = [
                "Ready"
            ]
            manifests = [
                platformv1alpha1.XStorageBucket{
                    metadata.name = "uptest-bucket-xr"
                    spec.parameters = {
                        acl = "private"
                        location = "US"
                        versioning: True
                    }
                }
            ]
            extraResources= [
                gcpv1beta1.ProviderConfig{
                    metadata.name = "default"
                    spec.projectID = "crossplane-playground"
                    spec.credentials = {
                        source = "Upbound"
                        upbound.federation = {
                            providerID = "projects/283222062215/locations/global/workloadIdentityPools/example-project-gcp-e2e/providers/upbound-oidc-provider"
                            serviceAccount = "example-project-gcp-e2e@crossplane-playground.iam.gserviceaccount.com"
                        }
                    }
                }
            ]
            skipDelete = False
            timeoutSeconds = 4500
        }
    }
]
items = _items