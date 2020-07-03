workspace(name = "macaron")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_proto_grpc",
    urls = ["https://github.com/rules-proto-grpc/rules_proto_grpc/archive/1.0.2.tar.gz"],
    sha256 = "5f0f2fc0199810c65a2de148a52ba0aff14d631d4e8202f41aff6a9d590a471b",
    strip_prefix = "rules_proto_grpc-1.0.2",
)

load("@rules_proto_grpc//:repositories.bzl", "rules_proto_grpc_toolchains", "rules_proto_grpc_repos")
load("@rules_proto_grpc//cpp:repositories.bzl", "cpp_repos")
load("@rules_proto_grpc//java:repositories.bzl", rules_proto_grpc_java_repos="java_repos")
load("@rules_proto_grpc//python:repositories.bzl", rules_proto_grpc_python_repos="python_repos")

rules_proto_grpc_toolchains()
rules_proto_grpc_repos()
cpp_repos()
rules_proto_grpc_java_repos()
rules_proto_grpc_python_repos()

http_archive(
    name = "io_bazel_rules_go",
    sha256 = "e88471aea3a3a4f19ec1310a55ba94772d087e9ce46e41ae38ecebe17935de7b",
    urls = [
        "https://storage.googleapis.com/bazel-mirror/github.com/bazelbuild/rules_go/releases/download/v0.20.3/rules_go-v0.20.3.tar.gz",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.20.3/rules_go-v0.20.3.tar.gz",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()

go_register_toolchains()

http_archive(
    name = "rules_python",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

http_archive(                                                                                       
    name = "rules_antlr",                                                                           
    sha256 = "26e6a83c665cf6c1093b628b3a749071322f0f70305d12ede30909695ed85591",                    
    strip_prefix = "rules_antlr-0.5.0",                                                             
    urls = ["https://github.com/marcohu/rules_antlr/archive/0.5.0.tar.gz"],                         
)                                                                                                   
                                                                                                    
load("@rules_antlr//antlr:lang.bzl", "C", "CPP", "GO", "JAVA", "OBJC", "PYTHON", "PYTHON2")         
load("@rules_antlr//antlr:repositories.bzl", "rules_antlr_dependencies")                            
                                                                                                    
rules_antlr_dependencies("2.7.7", 3, "4.8", C, CPP, GO, OBJC, PYTHON, PYTHON2)
