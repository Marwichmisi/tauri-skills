import Tauri

class ExamplePlugin: Plugin {
  @objc public func openCamera(_ invoke: Invoke) throws {
    invoke.resolve(["path": "/photo.jpg"])
  }
}
