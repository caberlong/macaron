load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")                                  
                                                                                                    
package(default_visibility = ["//macaron"])                                               
                                                                                                    
proto_library(                                                                                      
    name = "addressbook_proto",                                                                     
    srcs = ["addressbook.proto"],                                                                   
    deps = ["@com_google_protobuf//:timestamp_proto"]                                               
)                                                                                                   
                                                                                                    
cc_proto_library(                                                                                   
    name = "addressbook_cc_proto",                                                                  
    deps = [":addressbook_proto"],                                                                  
)                                                                                                   
                                                                                                    
python_proto_compile(                                                                               
    name = "addressbook_python_proto",                                                              
    deps = [":addressbook_proto"],                                                                  
)                                                                                                   
