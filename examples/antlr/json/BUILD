load("@rules_antlr//antlr:antlr4.bzl", "antlr")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

antlr(
    name = "json_antlr",
    srcs = ["JSON.g4"],
    language = "Python3",
)

py_library(
    name = "json_antlr_py",
    srcs = [":json_antlr"],
)

py_binary
