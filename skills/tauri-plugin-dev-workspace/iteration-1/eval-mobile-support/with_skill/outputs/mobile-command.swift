import Tauri

class OpenCameraArgs: Decodable {
  let source: String // requis : let Type
  var quality: Int? // optionnel : var Type?
  var allowEdit: Bool? // défaut NON supporté côté Decodable : nullable + défaut posé dans la commande
}

class MyPlugin: Plugin {
  @objc public func openCamera(_ invoke: Invoke) throws {
    let args = try invoke.parseArgs(OpenCameraArgs.self)
    // Défaut posé ici (doc) : arguments with default values are NOT supported
    let _quality = args.quality ?? 80
    let _allowEdit = args.allowEdit ?? false
    let _ = (_quality, _allowEdit, args.source)

    invoke.resolve(["path": "/photo.jpg"])
    trigger("camera", data: ["path": "/photo.jpg"])
  }

  // Permissions : override checkPermissions / requestPermissions uniquement si
  // permissions custom ; sinon Tauri fournit checkPermissions/requestPermissions auto.
}
