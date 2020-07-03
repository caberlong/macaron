load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_antlr//antlr:antlr4.bzl", "antlr")

antlr(
    name = "generated",
    srcs = ["JSON.g4"],
    language = "Python3",
)

py_library(
    name = "lib",
    srcs = [":generated"],
)

py_binary(
    name = "json",
    srcs = ["json.py"],
    imports = ["generated.py"],
    data = ["//antlr/json/testdata"],
    args = ["$(location //antlr/json/testdata)"],
    deps = [
        ":lib",
        "@antlr4_runtimes//:python",
    ],
)
