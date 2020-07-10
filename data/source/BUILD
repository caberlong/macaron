load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "generic_data_source",
    srcs = ["generic_data_source.py"],
		deps = [
			"//data/proto:data_python_proto",
			"@com_google_protobuf//:protobuf_python",
		]
)                                                                                                   

py_binary(                                                                                          
    name = "generic_data_source_test",                                                               
    srcs = ["generic_data_source_test.py"],                                                          
    deps = [                                                                                        
      ":generic_data_source",                                                        
    ],                                                                                              
)
