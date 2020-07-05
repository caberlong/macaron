load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   
load("@rules_antlr//antlr:antlr4.bzl", "antlr")                                                     

package (
		default_visibility = ["//:data_consumer"]
)
                                                                                                    
antlr(                                                                                              
    name = "json_antlr",                                                                             
    srcs = ["JSON.g4"],                                                                             
    language = "Python3",                                                                           
)                                                                                                   
                                                                                                    
py_library(                                                                                         
    name = "json_antlr_py",                                                                                   
    srcs = [":json_antlr"],                                                                          
)                                                                                                   

antlr(                                                                                              
    name = "yahoo_quote_antlr",                                                                             
    srcs = [
			"YahooQuoteLexer.g4",
			"YahooQuoteParser.g4",
		],                                                                             
    language = "Python3",                                                                           
)                                                                                                   
                                                                                                    
py_library(                                                                                         
    name = "yahoo_quote_antlr_py",                                                                                   
    srcs = [":yahoo_quote_antlr"],                                                                          
)                                                                                                   
