#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sdm660',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
    'vendor/xiaomi/sdm660-common',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib/hw/camera.sdm660.so': blob_fixup()
        .replace_needed('libcamera_sdm660_shim.so', 'libui_shim.so'),
    'vendor/lib64/libgf_ca.so': blob_fixup()
        .binary_regex_replace(b'/system/etc/firmware', b'/vendor/firmware\x00\x00\x00\x00'),
    ('vendor/lib64/libvendor.goodix.hardware.fingerprint@1.0.so', 'vendor/lib64/vendor.qti.hardware.fingerprint@1.0.so'): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'whyred',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common', module.vendor)
    utils.run()
