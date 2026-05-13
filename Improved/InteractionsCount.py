import cProfile
import pstats
import io

def run():
    from main import main
    main()

pr = cProfile.Profile()
pr.enable()
run()
pr.disable()

stream = io.StringIO()
stats = pstats.Stats(pr, stream=stream)

# ✅ filter to only YOUR files
stats.sort_stats("calls")
stats.print_stats("Original")   # only lines matching this path string

print(stream.getvalue())