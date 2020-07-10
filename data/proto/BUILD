load("@rules_proto_grpc//python:defs.bzl", "python_proto_library") 

package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
)

# Wrap all protos together for python inside //data. Otherwise they can't be imported properly.
python_proto_library(                                                                               
    name = "data_python_proto",                                                       
    deps = [
      ":fin_entity_proto",
      ":timeline_proto",
      ":data_proto",
      ":data_source_config_proto",
    ],
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
                                                                                                    
proto_library(                                                                                      
    name = "data_proto",                                                                     
    srcs = ["data.proto"],                                                                   
    deps = [
			":fin_entity_proto",
			":timeline_proto",
		]
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "data_cc_proto",                                                                  
    deps = [":data_proto"],                                                                  
)                                                                                                   
                                                                                                    
proto_library (                                                                                     
  name = "data_source_config_proto",                                                                
  srcs = ["data_source_config.proto"],                                                              
  deps = ["@com_google_protobuf//:any_proto"]                                                       
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "data_source_config_cc_proto",                                                           
    deps = [":data_source_config_proto"],                                                           
)                                                                                                   
                                                                                                    

