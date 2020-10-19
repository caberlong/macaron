load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
py_library(                                                                                         
    name = "predictor",
    srcs = ["predictor.py"],
		deps = [
      "//model/alpha_advantage:model_input",
      "//model/alpha_advantage:simple_lstm",
      "//data/example/alpha_advantage:normalized_example_generator",
		]
)                                                                                                   

py_binary(                                                                                          
    name = "predictor_test",                                                               
    srcs = ["predictor_test.py"],                                                          
    deps = [                                                                                        
      ":predictor",                                                        
    ],                                                                                              
)
