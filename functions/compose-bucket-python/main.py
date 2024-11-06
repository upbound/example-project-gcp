from crossplane.function import resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1
from model.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1
from model.io.upbound.gcp.storage.bucket import v1beta1 as bucketv1beta1
from model.io.upbound.gcp.storage.bucketacl import v1beta1 as aclv1beta1
from model.com.example.platform.xstoragebucket import v1alpha1

def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    observed_xr = v1alpha1.XStorageBucket(**req.observed.composite.resource)
    xr_name = observed_xr.metadata.name
    bucket_name = xr_name + "-bucket"
    params = observed_xr.spec.parameters

    bucket = bucketv1beta1.Bucket(
        apiVersion="storage.gcp.upbound.io/v1beta1",
        kind="Bucket",
        metadata=metav1.ObjectMeta(
            name=bucket_name,
        ),
        spec=bucketv1beta1.Spec(
            forProvider=bucketv1beta1.ForProvider(
                location=params.location,
                versioning=[bucketv1beta1.VersioningItem(
                    enabled=params.versioning,
                )],
            ),
        ),
    )
    resource.update(rsp.desired.resources[bucket.metadata.name], bucket)

    acl = aclv1beta1.BucketACL(
        apiVersion="storage.gcp.upbound.io/v1beta1",
        kind="BucketACL",
        metadata=metav1.ObjectMeta(
            name=xr_name + "-acl",
        ),
        spec=aclv1beta1.Spec(
            forProvider=aclv1beta1.ForProvider(
                bucketRef=aclv1beta1.BucketRef(
                    name=bucket_name,
                ),
                predefinedAcl=params.acl,
            ),
        ),
    )
    resource.update(rsp.desired.resources[acl.metadata.name], acl)
