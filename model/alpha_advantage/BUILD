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
    name = "model_input_int32",
    srcs = ["model_input_int32.py"],
		deps = [
		]
)                                                                                                   

py_binary(                                                                                          
    name = "model_input_int32_test",                                                               
    srcs = ["model_input_int32_test.py"],                                                          
    deps = [                                                                                        
      ":model_input_int32",                                                        
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
      ":model_input_int32",
      ":baseline_model",                                                        
    ],                                                                                              
)

py_library(                                                                                         
    name = "simple_lstm",
    srcs = ["simple_lstm.py"],
)                                                                                                   

py_binary(                                                                                          
    name = "simple_lstm_test",                                                               
    srcs = ["simple_lstm_test.py"],                                                          
    deps = [                                                                                        
      ":model_input",                                                        
      ":model_input_int32",
      ":simple_lstm",                                                        
    ],                                                                                              
)
