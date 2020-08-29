package(                                                                                            
  default_visibility = ["//:data_consumer"]                                                                   
) 

proto_library (
	name = "yahoo_quote_parser_config_proto",
	srcs = ["yahoo_quote_parser_config.proto"],                                                                   
)
                                                                                                    
cc_proto_library(                                                                                   
    name = "yahoo_quote_parser_config_cc_proto",                                                                  
    deps = [":yahoo_quote_parser_config_proto"],                                                                  
)                                                                                                   

proto_library (
	name = "alpha_advantage_source_config_proto",
	srcs = ["alpha_advantage_source_config.proto"],                                                                   
)
                                                                                                    
cc_proto_library(                                                                                   
    name = "alpha_advantage_source_config_cc_proto",                                                                  
    deps = [":alpha_advantage_source_config_proto"],                                                                  
)

proto_library (
	name = "alpha_advantage_parser_config_proto",
	srcs = ["alpha_advantage_parser_config.proto"],
  deps = ["@com_google_protobuf//:timestamp_proto"],
)
                                                                                                    
cc_proto_library(                                                                                   
    name = "alpha_advantage_parser_config_cc_proto",                                                                  
    deps = [":alpha_advantage_parser_config_proto"],                                                                  
)
