load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")                                  

package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
) 
                                                                                                    
proto_library(                                                                                      
    name = "activity_timestamp_proto",                                                                     
    srcs = ["activity_timestamp.proto"],                                                                   
    deps = ["@com_google_protobuf//:timestamp_proto"]                                               
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "activity_timestamp_cc_proto",                                                                  
    deps = [":activity_timestamp_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "activity_timestamp_python_proto",                                                              
    deps = [":activity_timestamp_proto"],                                                                  
)                                                                                                   

proto_library(                                                                                      
    name = "activity_proto",                                                                     
    srcs = ["activity.proto"],                                                                   
    deps = [
			":earning_activity_proto",
			":reorg_activity_proto",
			":trading_activity_proto",
		]
)

cc_proto_library(                                                                                   
    name = "activity_cc_proto",                                                                  
    deps = [":activity_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "activity_python_proto",                                                              
    deps = [":activity_proto"],                                                                  
)

proto_library(                                                                                      
    name = "earning_activity_proto",                                                                     
    srcs = ["earning_activity.proto"],                                                                   
    deps = [":activity_timestamp_proto"]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "earning_activity_cc_proto",                                                                  
    deps = [":earning_activity_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "earning_activity_python_proto",                                                              
    deps = [":earning_activity_proto"],                                                                  
)

proto_library(                                                                                      
    name = "reorg_activity_proto",                                                                     
    srcs = ["reorg_activity.proto"],                                                                   
    deps = [":activity_timestamp_proto"]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "reorg_activity_cc_proto",                                                                  
    deps = [":earning_activity_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "reorg_activity_python_proto",                                                              
    deps = [":earning_activity_proto"],                                                                  
)

proto_library(                                                                                      
    name = "trading_activity_proto",                                                                     
    srcs = ["trading_activity.proto"],                                                                   
    deps = [":activity_timestamp_proto"]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "trading_activity_cc_proto",                                                                  
    deps = [":earning_activity_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "trading_activity_python_proto",                                                              
    deps = [":earning_activity_proto"],                                                                  
)
