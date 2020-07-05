load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "yahoo_quote_parser_test",
    srcs = ["yahoo_quote_parser_test.py"],
    imports = ["../antlr/yahoo_quote_antlr.py"],
    # data = ["//data/source/html/testdata:yahoo_quote_gspc_html"],
    # args = ["$(location //data/source/html/testdata:yahoo_quote_gspc_html)"],
    data = ["//data/source/html/testdata:yahoo_quote_gspc_html"],
    args = ["$(location //data/source/html/testdata:yahoo_quote_gspc_html)"],
    deps = [
				"//data/source/antlr:yahoo_quote_antlr_py",
        "@antlr4_runtimes//:python",
    ],
)
