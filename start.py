from scrapy import cmdline


print("[Spider] running...")

cmdline.execute("scrapy crawl shixiseng".split())

print("[Spider] done")