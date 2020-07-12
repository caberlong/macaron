load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "yahoo_quote_parser",
    srcs = ["yahoo_quote_parser.py"],
    imports = ["../../antlr/yahoo_quote/yahoo_quote_antlr.py"],
    deps = [
				"//data/antlr/yahoo_quote:yahoo_quote_antlr_py",
        "//data/proto:data_python_proto",
        "@antlr4_runtimes//:python",
    ],
)

py_binary(
    name = "yahoo_quote_parser_test",
    srcs = ["yahoo_quote_parser_test.py"],
    # data = ["//data/source/html/testdata:yahoo_quote_gspc_html"],
    # args = ["$(location //data/source/html/testdata:yahoo_quote_gspc_html)"],
    data = ["//data/source/html/testdata:yahoo_quote_microsoft_html"],
    args = ["$(location //data/source/html/testdata:yahoo_quote_microsoft_html)"],
    deps = [
        ":yahoo_quote_parser",
        "//data/proto:data_python_proto",
        "@com_google_protobuf//:protobuf_python",
    ],
)
