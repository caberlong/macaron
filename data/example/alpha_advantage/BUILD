load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "normalized_example_generator",
    srcs = ["normalized_example_generator.py"],
		deps = [
			"//proto:data_python_proto",
			"//data/utils:data_proto_generator",
      "@com_google_protobuf//:protobuf_python",
		]
)                                                                                                   

py_binary(                                                                                          
    name = "normalized_example_generator_test",                                                               
    srcs = ["normalized_example_generator_test.py"],                                                          
    deps = [                                                                                        
      ":normalized_example_generator",                                                        
	    "//data/utils:data_proto_generator",
    ],                                                                                              
)

py_binary(                                                                                          
    name = "normalized_example_generator_run",                                                               
    srcs = ["normalized_example_generator_run.py"],                                                          
    deps = [                                                                                        
      ":normalized_example_generator",                                                        
      "//data/source/alpha_advantage:alpha_advantage_downloader_run_lib", 
	    "//data/utils:data_proto_generator",
      "@com_google_protobuf//:protobuf_python",
    ],                                                                                              
)
