from .model.io.upbound.dev.meta.compositiontest import v1alpha1 as compositiontest
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from .model.com.example.platform.xstoragebucket import v1alpha1 as platformv1alpha1
from .model.io.upbound.gcp.storage.bucketacl import v1beta1 as bucketaclv1beta1
from .model.io.upbound.gcp.storage.bucket import v1beta1 as bucketv1beta1

xStorageBucket = platformv1alpha1.XStorageBucket(
    apiVersion="platform.example.com/v1alpha1",
    kind="XStorageBucket",
    metadata=k8s.ObjectMeta(
        name="example-python"
    ),
    spec = platformv1alpha1.Spec(
        compositionSelector=platformv1alpha1.CompositionSelector(
            matchLabels={
                "language": "python",
            },
        ),
        parameters = platformv1alpha1.Parameters(
            acl="publicRead",
            location="US",
            versioning=True,
        ),
    ),
)

bucket = bucketv1beta1.Bucket(
    apiVersion="storage.gcp.upbound.io/v1beta1",
    kind="Bucket",
    metadata=k8s.ObjectMeta(
        name="example-python-bucket",
    ),
    spec=bucketv1beta1.Spec(
        forProvider=bucketv1beta1.ForProvider(
            location="US"
        )
    )
)

bucket_acl = bucketaclv1beta1.BucketACL(
    apiVersion="storage.gcp.upbound.io/v1beta1",
    kind="BucketACL",
    metadata=k8s.ObjectMeta(
        name="example-python-acl",
    ),
    spec=bucketaclv1beta1.Spec(
        forProvider=bucketaclv1beta1.ForProvider(
            bucket="example-python-acl",
            predefinedAcl="publicRead",
        ),
    ),
)

test = compositiontest.CompositionTest(
    metadata=k8s.ObjectMeta(
        name="test-xstoragebucket-python",
    ),
    spec = compositiontest.Spec(
        assertResources=[
            xStorageBucket.model_dump(exclude_unset=True),
            # TODO: Assert other resources. This is tricker for Python than KCL
            # since we let Crossplane name our resources.
        ],
        compositionPath="apis/python/composition.yaml",
        xrPath="examples/python/example.yaml",
        xrdPath="apis/xstoragebuckets/definition.yaml",
        timeoutSeconds=120,
        validate=False,
    )
)
