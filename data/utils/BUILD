load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "data_proto_generator",
    srcs = ["data_proto_generator.py"],
    imports = ["../antlr/data_generator/data_generator_antlr.py"],                                                 
		deps = [
			"//data/antlr/data_generator:data_generator_antlr_py",
			"//data/proto:data_python_proto",
      "@com_google_protobuf//:protobuf_python",
			"@antlr4_runtimes//:python",                                                                
		]
)                                                                                                   

py_binary(                                                                                          
    name = "data_proto_generator_test",                                                               
    srcs = ["data_proto_generator_test.py"],                                                          
    deps = [                                                                                        
        ":data_proto_generator",                                                        
    ],                                                                                              
)
