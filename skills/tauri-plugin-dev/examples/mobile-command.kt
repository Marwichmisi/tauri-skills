import android.app.Activity
import app.tauri.annotation.Command
import app.tauri.annotation.TauriPlugin
import app.tauri.plugin.Invoke
import app.tauri.plugin.JSObject

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    val ret = JSObject()
    ret.put("path", "/photo.jpg")
    invoke.resolve(ret)
  }
}
