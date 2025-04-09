import models.io.upbound.gcp.storage.v1beta1
import models.com.example.platform.v1alpha1.xstoragebucket as xstoragebucketv1alpha1

oxr = xstoragebucketv1alpha1.XStorageBucket{**option("params").oxr} # observed composite resource
bucketName = "{}-bucket".format(oxr.metadata.name.lower())

_metadata = lambda name: str -> any {
  {
    name = name
    annotations = {
      "krm.kcl.dev/composition-resource-name" = name
    }
  }
}

_items: [any] = [
    v1beta1.Bucket{
        metadata: _metadata(bucketName)
        spec = {
            forProvider = {
                location = oxr.spec.parameters.location
                versioning = [
                    {
                        enabled = oxr.spec.parameters.versioning
                    }
                ]
            }
        }
    },
    v1beta1.BucketACL{
        metadata: _metadata("{}-acl".format(oxr.metadata.name))
        spec = {
            forProvider = {
                bucketRef = {
                    name = bucketName
                }
                predefinedAcl = oxr.spec.parameters.acl
            }
        }
    }
]

items = _items
