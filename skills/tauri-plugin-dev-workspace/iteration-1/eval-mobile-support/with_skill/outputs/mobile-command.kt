import android.app.Activity
import app.tauri.annotation.Command
import app.tauri.annotation.InvokeArg
import app.tauri.annotation.TauriPlugin
import app.tauri.plugin.Invoke
import app.tauri.plugin.JSObject
import app.tauri.plugin.Plugin

@TauriPlugin
class MyPlugin(private val activity: Activity) : Plugin(activity) {

  @InvokeArg
  internal class OpenCameraArgs {
    lateinit var source: String // requis : lateinit var Type
    var quality: Int? = null // optionnel : var Type? = null
    var allowEdit: Boolean = false // défaut : var Type = default-value
  }

  @Command
  fun openCamera(invoke: Invoke) {
    val args = invoke.parseArgs(OpenCameraArgs::class.java)
    // args.source (requis), args.quality (optionnel), args.allowEdit (défaut false)
    // Note main-thread : ne pas bloquer ; pour IO utiliser CoroutineScope(Dispatchers.IO).launch { ... }
    val ret = JSObject()
    ret.put("path", "/photo.jpg")
    invoke.resolve(ret)

    val payload = JSObject()
    payload.put("path", "/photo.jpg")
    trigger("camera", payload)
  }
}
