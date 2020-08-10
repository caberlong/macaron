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

py_library(                                                                                         
    name = "vocabulary",
    srcs = ["vocabulary.py"],
		deps = [
      ":model_input"
		]
)                                                                                                   

py_binary(                                                                                          
    name = "vocabulary_test",                                                               
    srcs = ["vocabulary_test.py"],                                                          
    deps = [                                                                                        
      ":vocabulary",                                                        
    ],                                                                                              
)

py_library(                                                                                         
    name = "baseline_model",
    srcs = ["baseline_model.py"],
)                                                                                                   

py_binary(                                                                                          
    name = "baseline_model_test",                                                               
    srcs = ["baseline_model_test.py"],                                                          
    deps = [                                                                                        
      ":model_input",                                                        
      ":baseline_model",                                                        
    ],                                                                                              
)

py_library(                                                                                         
    name = "linear_model",
    srcs = ["linear_model.py"],
)                                                                                                   

py_binary(                                                                                          
    name = "linear_model_test",                                                               
    srcs = ["linear_model_test.py"],                                                          
    deps = [                                                                                        
      ":model_input",                                                        
      ":linear_model",                                                        
    ],                                                                                              
)
