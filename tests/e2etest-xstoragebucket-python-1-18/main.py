from .model.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from .model.com.example.platform.xstoragebucket import v1alpha1 as xstoragebucket
from .model.io.upbound.gcp.providerconfig import v1beta1 as providerconfig

bucket_manifest = xstoragebucket.XStorageBucket(
    metadata=k8s.ObjectMeta(
        name="uptest-bucket-xr",
    ),
    spec=xstoragebucket.Spec(
        parameters=xstoragebucket.Parameters(
            acl="private",
            location="US",
            versioning=True,
        ),
    ),
)

provider_config = providerconfig.ProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=providerconfig.Spec(
        projectID="crossplane-playground",
        credentials=providerconfig.Credentials(
            source="Upbound",
            upbound=providerconfig.Upbound(
                federation=providerconfig.Federation(
                    providerID="projects/283222062215/locations/global/workloadIdentityPools/example-project-gcp-e2e/providers/upbound-oidc-provider",
                    serviceAccount="example-project-gcp-e2e@crossplane-playground.iam.gserviceaccount.com",
                ),
            ),
        ),
    ),
)

test = e2etest.E2ETest(
    metadata=k8s.ObjectMeta(
        name="e2etest-xstoragebucket-python",
    ),
    spec=e2etest.Spec(
        crossplane=e2etest.Crossplane(
            autoUpgrade=e2etest.AutoUpgrade(
                channel=e2etest.Channel.None_,
            ),
            version="1.18.3-up.1",
        ),
        defaultConditions=[
            "Ready",
        ],
        manifests=[bucket_manifest.model_dump()],
        extraResources=[provider_config.model_dump()],
        skipDelete=False,
        timeoutSeconds=4500,
    )
)
