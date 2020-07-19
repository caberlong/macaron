load("@rules_python//python:defs.bzl", "py_binary", "py_library")                                   
load("@rules_antlr//antlr:antlr4.bzl", "antlr")                                                     

package (
		default_visibility = ["//:data_consumer"]
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
    imports = ["yahoo_quote_antlr.py"],                                                 
    srcs = [":yahoo_quote_antlr"],                                                                          
)                                                                                                   

py_binary(                                                                                          
    name = "yahoo_quote_test",                                                               
    srcs = ["yahoo_quote_test.py"],                                                          
    # data = ["//data/antlr/yahoo_quote/testdata:yahoo_quote_gspc_html"],                                 
    # args = ["$(location //data/antlr/yahoo_quote/testdata:yahoo_quote_gspc_html)"],                     
    data = ["//data/antlr/yahoo_quote/testdata:yahoo_quote_microsoft_html"],                              
    args = ["$(location //data/antlr/yahoo_quote/testdata:yahoo_quote_microsoft_html)"],                  
    deps = [                                                                                        
        ":yahoo_quote_antlr_py",                                                        
        "@antlr4_runtimes//:python",                                                                
    ],                                                                                              
)
