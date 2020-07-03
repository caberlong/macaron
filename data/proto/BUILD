load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")                                  

package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
)

proto_library(                                                                                      
    name = "fin_entity_proto",                                                                     
    srcs = ["fin_entity.proto"],                                                                   
    deps = ["//data/proto/trait:trait_proto"]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "fin_entity_cc_proto",                                                                  
    deps = [":fin_entity_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "fin_entity_python_proto",                                                              
    deps = [":fin_entity_proto"],                                                                  
)

proto_library(                                                                                      
    name = "timeline_proto",                                                                     
    srcs = ["timeline.proto"],                                                                   
    deps = [
			"//data/proto/activity:activity_proto",
			"@com_google_protobuf//:timestamp_proto",
		]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "timeline_cc_proto",                                                                  
    deps = [":timeline_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "timeline_python_proto",                                                              
    deps = [":timeline_proto"],                                                                  
)
