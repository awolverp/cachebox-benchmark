from lib import get_benchmark

import cachebox
if tuple(int(i) for i in cachebox.__version__.split(".")) < (1, 0, 21):
    cachebox.TTLCache.__module__ = "cachebox._cachebox"
    cachebox.TTLCacheNoDefault.__module__ = "cachebox._cachebox"

def main():
    import sys

    multibenchmarks = []

    for classname in sys.argv[1:]:
        multibenchmarks.append(
            (classname, get_benchmark(classname))
        )

    for classname, b in multibenchmarks:
        print("###", classname, "\n")
        print(b.to_markdown())

if __name__ == "__main__":
    main()
