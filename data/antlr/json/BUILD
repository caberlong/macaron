load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   
load("@rules_antlr//antlr:antlr4.bzl", "antlr")                                                     

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
antlr(                                                                                              
    name = "json_antlr",
    srcs = [
			"JSON.g4",
		],                                                                             
    language = "Python3",                                                                           
)                                                                                                   
                                                                                                    
py_library(                                                                                         
    name = "json_antlr_py",                                                                                   
    imports = ["json_antlr.py"],                                                 
    srcs = [":json_antlr"],                                                                          
)                                                                                                   

py_binary(                                                                                          
    name = "json_test",                                                               
    srcs = ["json_test.py"],                                                          
    data = ["//data/antlr/json/testdata:appl_json"],                              
    args = ["$(location //data/antlr/json/testdata:appl_json)"],                  
    deps = [                                                                                        
        ":json_antlr_py",                                                        
        "@antlr4_runtimes//:python",                                                                
    ],                                                                                              
)
