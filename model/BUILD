load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "model_input",
    srcs = ["model_input.py"],
		deps = [
		]
)                                                                                                   

py_binary(                                                                                          
    name = "model_input_test",                                                               
    srcs = ["model_input_test.py"],                                                          
    deps = [                                                                                        
      ":model_input",                                                        
    ],                                                                                              
)
