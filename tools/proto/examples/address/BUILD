load("@rules_proto_grpc//python:defs.bzl", "python_proto_compile")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "addressbook_proto",
    srcs = ["addressbook.proto"],
    deps = ["@com_google_protobuf//:timestamp_proto"]
)

cc_proto_library(
    name = "addressbook_cc_proto",
    deps = [":addressbook_proto"],
)

java_proto_library(
    name = "addressbook_java_proto",
    deps = [":addressbook_proto"],
)

python_proto_compile(
    name = "addressbook_python_proto",
    deps = [":addressbook_proto"],
)

cc_proto_library(
    name = "person_cc_proto",
    deps = [":person_proto"],
)

java_proto_library(
    name = "person_java_proto",
    deps = [":person_proto"],
)

python_proto_compile(
    name = "person_python_proto",
    deps = [":person_proto"],
)

proto_library(
    name = "person_proto",
    srcs = ["person.proto"],
    deps = [
        ":address_proto",
        # Well known protos should be included as deps in the
        # proto_library rules of the source files importing them.
        # A list of all @com_google_protobuf well known protos can
        # seen with:
        # `bazel query 'kind(proto_library, @com_google_protobuf//:all)'`
        "@com_google_protobuf//:any_proto",
    ],
)

proto_library(
    name = "address_proto",
    srcs = ["address.proto"],
    deps = [":zip_code_proto"],
)

proto_library(
    name = "zip_code_proto",
    srcs = ["zip_code.proto"],
)
