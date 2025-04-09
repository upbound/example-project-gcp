import models.com.example.platform.v1alpha1 as platformv1alpha1
import models.io.upbound.gcp.storage.v1beta1 as storagev1beta1
import models.io.upbound.dev.meta.v1alpha1 as metav1alpha1

_items = [
    metav1alpha1.CompositionTest{
        metadata.name="test-xstoragebucket-kcl"
        spec= {
            assertResources: [
                platformv1alpha1.XStorageBucket{
                    metadata.name: "example-kcl"
                    spec: {
                        parameters: {
                            acl: "publicRead"
                            location: "US"
                            versioning: True
                        }
                        compositionSelector:{
                            matchLabels: {
                                language: "kcl"
                            }
                        }
                    }
                }
                storagev1beta1.BucketACL{
                    metadata.name: "example-kcl-acl"
                    spec.forProvider:{
                        predefinedAcl: "publicRead"
                        bucketRef: {
                            name: "example-kcl-bucket"
                        }
                    }
                }
                storagev1beta1.Bucket{
                    metadata.name: "example-kcl-bucket"
                    spec.forProvider: {
                        location: "US"
                        versioning: [{
                            enabled: True
                        }]
                    }
                }
            ]
            compositionPath: "apis/kcl/composition.yaml"
            xrPath: "examples/kcl/example.yaml"
            xrdPath: "apis/xstoragebuckets/definition.yaml"
            timeoutSeconds: 120
            validate: False
        }
    }
]
items = _items
