load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")                                  

package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
) 

proto_library (
	name = "parser_config_proto",
	srcs = ["parser_config.proto"],                                                                   
  deps = ["@com_google_protobuf//:any_proto"]                                               
)
                                                                                                    
cc_proto_library(                                                                                   
    name = "parser_config_cc_proto",                                                                  
    deps = [":parser_config_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "parser_config_python_proto",                                                              
    deps = [":parser_config_proto"],                                                                  
)                                                                                                   

proto_library (
	name = "parser_output_proto",
	srcs = ["parser_output.proto"],                                                                   
  deps = [
		"//data/proto:fin_entity_proto",
		"//data/proto:timeline_proto",
	]
)
                                                                                                    
cc_proto_library(                                                                                   
    name = "parser_output_cc_proto",                                                                  
    deps = [":parser_output_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "parser_output_python_proto",                                                              
    deps = [":parser_output_proto"],                                                                  
)
