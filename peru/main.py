#! /usr/bin/env python3

import os
import sys

from .cache import Cache
from .local_module import LocalModule
from .parser import Parser
from .resolver import Resolver
from .runtime import Runtime


def main():
    peru_file = os.getenv("PERU_FILE") or "peru.yaml"
    if not os.path.isfile(peru_file):
        print(peru_file + " not found.")
        sys.exit(1)
    cache_root = os.getenv("PERU_CACHE") or ".peru-cache"
    cache = Cache(cache_root)
    runtime = Runtime(cache)
    parser = Parser(runtime.plugins)
    scope, imports = parser.parse_file(peru_file)
    resolver = Resolver(scope, cache)
    local_module = LocalModule(imports)

    local_module.apply_imports(resolver)
    if len(sys.argv) > 1:
        for target_str in sys.argv[1:]:
            local_module.do_build(resolver, target_str)