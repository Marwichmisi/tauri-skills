package com.plugin.myplugin

import android.app.Activity
import app.tauri.plugin.Command
import app.tauri.plugin.Invoke
import app.tauri.plugin.Plugin
import app.tauri.plugin.JSObject

class MyPluginPlugin(activity: Activity) : Plugin(activity) {

    @Command
    fun openCamera(invoke: Invoke) {
        val quality = invoke.getString("quality")
            ?: return invoke.reject("quality est requis")
        val flash = invoke.getBoolean("flash")
        val mode = invoke.getString("mode", "auto")!!

        val ret = JSObject()
        ret.put("path", "/tmp/photo.jpg")
        ret.put("quality", quality)
        invoke.resolve(ret)
    }
}
