import models.v1beta1 as v1beta1

oxr = option("params").oxr # observed composite resource

bucketName = "{}-bucket".format(oxr.metadata.name)
_items: [any] = [
    v1beta1.Bucket{
        metadata.name = bucketName
        spec = v1beta1.StorageGcpUpboundIoV1beta1BucketSpec{
            forProvider = v1beta1.StorageGcpUpboundIoV1beta1BucketSpecForProvider{
                location = oxr.spec.location
                versioning = [
                    v1beta1.StorageGcpUpboundIoV1beta1BucketSpecForProviderVersioningItems0{
                        enabled = oxr.spec.versioning
                    }
                ]
            }
        }
    },
    v1beta1.BucketACL{
        metadata.name = "{}-acl".format(oxr.metadata.name)
        spec = v1beta1.StorageGcpUpboundIoV1beta1BucketACLSpec{
            forProvider = v1beta1.StorageGcpUpboundIoV1beta1BucketACLSpecForProvider{
                bucketRef = v1beta1.StorageGcpUpboundIoV1beta1BucketACLSpecForProviderBucketRef{
                    name = bucketName
                }
                predefinedAcl = oxr.spec.acl
            }
        }
    }
]

items = _items
