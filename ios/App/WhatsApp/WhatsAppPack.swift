import Foundation

enum WhatsAppPackError: LocalizedError {
    case missingTray(String)
    case missingSticker(String)
    case sendFailed

    var errorDescription: String? {
        switch self {
        case .missingTray(let identifier):
            return "Missing tray image for pack \(identifier). Build the app in Xcode so derived WhatsApp assets are copied into the bundle."
        case .missingSticker(let slug):
            return "Missing WhatsApp WebP for \(slug). Build the app in Xcode so derived WhatsApp assets are copied into the bundle."
        case .sendFailed:
            return "Could not copy the sticker pack to WhatsApp."
        }
    }
}

enum WhatsAppPack {
    static let bundleDirectory = "WhatsAppStickers"

    static func send(_ pack: PackLibrary.Pack, bundle: Bundle = .main) throws {
        let json = try pasteboardJSON(for: pack, bundle: bundle)
        guard Interoperability.send(json: json) else {
            throw WhatsAppPackError.sendFailed
        }
    }

    static func pasteboardJSON(for pack: PackLibrary.Pack, bundle: Bundle = .main) throws -> [String: Any] {
        guard let trayURL = bundle.url(
            forResource: "tray",
            withExtension: "png",
            subdirectory: "\(bundleDirectory)/\(pack.identifier)"
        ) else {
            throw WhatsAppPackError.missingTray(pack.identifier)
        }

        let trayImage = try Data(contentsOf: trayURL).base64EncodedString()
        var stickers: [[String: Any]] = []

        for sticker in pack.stickers {
            guard let webpURL = bundle.url(
                forResource: sticker.slug,
                withExtension: "webp",
                subdirectory: "\(bundleDirectory)/\(pack.identifier)"
            ) else {
                throw WhatsAppPackError.missingSticker(sticker.slug)
            }

            stickers.append([
                "image_data": try Data(contentsOf: webpURL).base64EncodedString(),
                "emojis": sticker.emojis,
                "accessibility_text": String(sticker.accessibilityText.prefix(125))
            ])
        }

        return [
            "identifier": pack.identifier,
            "name": pack.name,
            "publisher": pack.publisher,
            "tray_image": trayImage,
            "stickers": stickers
        ]
    }
}
