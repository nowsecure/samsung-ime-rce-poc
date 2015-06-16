from zipfile import ZipFile
import androguard.core.bytecodes.dvm
import sys
import struct

def get_dos_time(date_time_tuple):
  dt = date_time_tuple
  dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
  dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
  return (dosdate << 16) | dostime

def print_odex_info(odex_file):
  d = androguard.core.bytecodes.dvm.DalvikOdexVMFormat(open(odex_file, "r").read())
  print "modTime: " + hex(d.get_dependencies().modification_time)
  print "crc: " + hex(d.get_dependencies().crc)
  print "dalvik build ver: " + hex(d.get_dependencies().dalvik_build)

def patch_odex(originalAPK, odex_in, odex_out):
  #Extract the CRC value and modification time from the zip
  #set them in the odex file write the modded odex file
  with ZipFile(targetAPK, 'r') as myzip:
    odex_buff = open(odexFile, "r").read()
    o_dependencies_offset =  struct.unpack("=I", odex_buff[16:20])[0]
    o_mt_offset = o_dependencies_offset
    o_crc_offset = o_mt_offset + 4
    o_vm_build_ver_offset = o_crc_offset + 4
    o_mod_time = struct.unpack("=I", odex_buff[o_mt_offset:o_mt_offset+4])[0]
    o_crc = struct.unpack("=I", odex_buff[o_crc_offset:o_crc_offset+4])[0]
    o_vm_build_ver = struct.unpack("=I", odex_buff[o_vm_build_ver_offset:o_vm_build_ver_offset+4])[0]

    vm_build_ver = 28
    vm_build_ver = o_vm_build_ver

    info = myzip.getinfo('classes.dex')
    apk_time = get_dos_time(info.date_time)

    print "Original modTime: " + hex(o_mod_time)
    print "Original CRC: " + hex(o_crc)
    print "Apk ModTime: "  + hex(apk_time)
    print "APK classes CRC: " + hex(info.CRC)

    patched_buff = odex_buff[:o_mt_offset] + \
                           struct.pack("=I", apk_time) + \
                           struct.pack("=I", info.CRC) + \
                           struct.pack("=I", vm_build_ver) + \
                   odex_buff[o_vm_build_ver_offset+4:]

    patched_odex = open(outputFile, "w")
    patched_odex.write(patched_buff)
    patched_odex.close()

def usage():
  print "patch <ODEX_TO_PATCH> <TARGET_APK> <OUTPUT_ODEX>"
  print "print <ODEX_FILE>"

if __name__ == "__main__":
  if len(sys.argv) < 2:
     usage()
     sys.exit(-1)

  if sys.argv[1] == "print":
    print_odex_info(sys.argv[2])
  elif sys.argv[1] == "patch":
    odexFile = sys.argv[2]
    targetAPK = sys.argv[3]
    outputFile = "patched.odex"
    patch_odex(targetAPK, odexFile, outputFile)
  else:
    print "A"
