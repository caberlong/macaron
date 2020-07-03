load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_antlr//antlr:antlr4.bzl", "antlr")

antlr(
    name = "generated",
    srcs = ["Hello.g4"],
    language = "Python3",
)

py_library(
    name = "lib",
    srcs = [":generated"],
)

py_binary(
    name = "hello",
    srcs = ["hello.py"],
    imports = ["generated.py"],
    data = ["//antlr/hello/testdata"],
    args = ["$(location //antlr/hello/testdata)"],
    deps = [
        ":lib",
        "@antlr4_runtimes//:python",
    ],
)
