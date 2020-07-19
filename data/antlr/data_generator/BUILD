load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   
load("@rules_antlr//antlr:antlr4.bzl", "antlr")                                                     

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
antlr(                                                                                              
    name = "data_generator_antlr",                                                                             
    srcs = [
			"DataGeneratorLexer.g4",
			"DataGeneratorParser.g4",
		],                                                                             
    layout = "src/tmp",
    # package="data.antlr.data_generator",
    language = "Python3",                                                                           
)                                                                                                   
                                                                                                    
py_library(                                                                                         
    name = "data_generator_antlr_py",                                                                                   
    srcs = [":data_generator_antlr"],                                                                          
    imports = ["data_generator_antlr.py"]
)                                                                                                   

py_binary(                                                                                          
    name = "data_generator_test",                                                               
    srcs = ["data_generator_test.py"],                                                          
    data = ["//data/antlr/data_generator/testdata:data_generator_config"],                              
    args = ["$(location //data/antlr/data_generator/testdata:data_generator_config)"],                  
    deps = [                                                                                        
        ":data_generator_antlr_py",                                                        
        "@antlr4_runtimes//:python",                                                                
    ],                                                                                              
)
