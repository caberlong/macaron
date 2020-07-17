load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "generic_data_generator",
    srcs = ["generic_data_generator.py"],
		deps = [
			"//proto:data_python_proto",
			"@com_google_protobuf//:protobuf_python",
		]
)                                                                                                   

py_binary(                                                                                          
    name = "generic_data_generator_test",                                                               
    srcs = ["generic_data_generator_test.py"],                                                          
    deps = [                                                                                        
      ":generic_data_generator",                                                        
			"//data/utils:data_proto_generator",
			"//proto:data_python_proto",
    ],                                                                                              
)
