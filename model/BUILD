load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "example_generator",
    srcs = ["example_generator.py"],
		deps = [
			"//proto:data_python_proto",
			"//data/utils:data_proto_generator",
      "@com_google_protobuf//:protobuf_python",
		]
)                                                                                                   

py_binary(                                                                                          
    name = "example_generator_test",                                                               
    srcs = ["example_generator_test.py"],                                                          
    deps = [                                                                                        
      ":example_generator",                                                        
	    "//data/utils:data_proto_generator",
    ],                                                                                              
)
