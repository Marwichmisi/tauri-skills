import Tauri

struct OpenCameraArgs: Decodable {
    let quality: String
    let flash: Bool?
    var mode: String = "auto"

    enum CodingKeys: String, CodingKey {
        case quality, flash, mode
    }

    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        quality = try c.decode(String.self, forKey: .quality)
        flash = try c.decodeIfPresent(Bool.self, forKey: .flash)
        mode = try c.decodeIfPresent(String.self, forKey: .mode) ?? "auto"
    }
}

class MyPluginPlugin: Plugin {
    @objc func openCamera(_ invoke: Invoke) throws {
        let args = try invoke.parseArgs(OpenCameraArgs.self)
        invoke.resolve(["path": "/tmp/photo.jpg", "quality": args.quality])
    }
}
