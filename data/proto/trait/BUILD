load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")                                  

package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
) 

proto_library (
	name = "trait_proto",
	srcs = ["trait.proto"],                                                                   
	deps = [
		":common_trait_proto",
		":geo_trait_proto",
		":demo_trait_proto",
		":sector_trait_proto",
	]
)
                                                                                                    
proto_library(                                                                                      
    name = "common_trait_proto",                                                                     
    srcs = ["common_trait.proto"],                                                                   
    deps = ["@com_google_protobuf//:timestamp_proto"]                                               
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "common_trait_cc_proto",                                                                  
    deps = [":common_trait_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "common_trait_python_proto",                                                              
    deps = [":common_trait_proto"],                                                                  
)                                                                                                   

proto_library(                                                                                      
    name = "demo_trait_proto",                                                                     
    srcs = ["demo_trait.proto"],                                                                   
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "demo_trait_cc_proto",                                                                  
    deps = [":demo_trait_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "demo_trait_python_proto",                                                              
    deps = [":demo_trait_proto"],                                                                  
)

proto_library(                                                                                      
    name = "geo_trait_proto",                                                                     
    srcs = ["geo_trait.proto"],                                                                   
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "geo_trait_cc_proto",                                                                  
    deps = [":geo_trait_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "geo_trait_python_proto",                                                              
    deps = [":geo_trait_proto"],                                                                  
)

proto_library(                                                                                      
    name = "sector_trait_proto",                                                                     
    srcs = ["sector_trait.proto"],                                                                   
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "sector_trait_cc_proto",                                                                  
    deps = [":sector_trait_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "sector_trait_python_proto",                                                              
    deps = [":sector_trait_proto"],                                                                  
)
