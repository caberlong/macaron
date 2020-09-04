load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@subpar//:subpar.bzl", "par_binary")

py_library(
    name = "alpha_advantage_downloader",
    srcs = ["alpha_advantage_downloader.py"],
    deps = [
        "//proto:data_python_proto",
    ],
)

py_binary(
    name = "alpha_advantage_downloader_test",
    srcs = ["alpha_advantage_downloader_test.py"],
    deps = [
        ":alpha_advantage_downloader",
        "//proto:data_python_proto",
    ],
)

py_library(
    name = "alpha_advantage_downloader_run_lib",
    srcs = ["alpha_advantage_downloader_run.py"],
    deps = [
        ":alpha_advantage_downloader",
        "//proto:data_python_proto",
    ],
)

par_binary(
    name = "alpha_advantage_downloader_run",
    srcs = ["alpha_advantage_downloader_run.py"],
    deps = [
        ":alpha_advantage_downloader",
        "//proto:data_python_proto",
    ],
)

py_library(
    name = "alpha_advantage_parser",
    srcs = ["alpha_advantage_parser.py"],
    deps = [
				"//data/antlr/json:json_antlr_py",
        "//proto:data_python_proto",
        "//data/utils:data_proto_generator",
        "@antlr4_runtimes//:python",
    ],
)

py_binary(
    name = "alpha_advantage_parser_test",
    srcs = ["alpha_advantage_parser_test.py"],
    deps = [
        ":alpha_advantage_parser",
        "//proto:data_python_proto",
        "@com_google_protobuf//:protobuf_python",
    ],
)

py_binary(
    name = "alpha_advantage_parser_run",
    srcs = ["alpha_advantage_parser_run.py"],
    deps = [
        ":alpha_advantage_parser",
        ":alpha_advantage_downloader_run_lib",
        "//proto:data_python_proto",
        "@com_google_protobuf//:protobuf_python",
    ],
)
