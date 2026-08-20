import Foundation
import UIKit

struct PackConfig: Decodable, Equatable {
    let publisher: String
    let iosAppStoreID: String
    let traySlug: String
    let emojis: [String: [String]]
    let whatsappPacks: [WhatsAppPackDefinition]

    enum CodingKeys: String, CodingKey {
        case publisher
        case iosAppStoreID = "ios_app_store_id"
        case traySlug = "tray_slug"
        case emojis
        case whatsappPacks = "whatsapp_packs"
    }

    var iosAppStoreLink: String {
        "https://apps.apple.com/app/id\(iosAppStoreID)"
    }
}

struct WhatsAppPackDefinition: Decodable, Identifiable, Equatable {
    let identifier: String
    let name: String
    let slugs: [String]

    var id: String { identifier }
}

enum PackLibraryError: LocalizedError {
    case missingConfig
    case unreadableConfig(Error)

    var errorDescription: String? {
        switch self {
        case .missingConfig:
            return "pack-config.json is missing from the app bundle. Build TT Stickers in Xcode so the export script can copy it."
        case .unreadableConfig(let error):
            return "Could not read pack-config.json: \(error.localizedDescription)"
        }
    }
}

struct PackLibrary {
    static let previewDirectory = "PreviewStickers"

    let config: PackConfig
    let packs: [Pack]

    struct Pack: Identifiable {
        let identifier: String
        let name: String
        let publisher: String
        let stickers: [StickerPreview]

        var id: String { identifier }

        var slugs: [String] { stickers.map(\.slug) }
    }

    struct StickerPreview: Identifiable {
        let slug: String
        let emojis: [String]
        let previewImage: UIImage?
        let accessibilityText: String

        var id: String { slug }
    }

    static func load(from bundle: Bundle = .main) throws -> PackLibrary {
        guard let url = bundle.url(forResource: "pack-config", withExtension: "json") else {
            throw PackLibraryError.missingConfig
        }

        let config: PackConfig
        do {
            config = try JSONDecoder().decode(PackConfig.self, from: Data(contentsOf: url))
        } catch {
            throw PackLibraryError.unreadableConfig(error)
        }

        let packs = config.whatsappPacks.map { definition in
            Pack(
                identifier: definition.identifier,
                name: definition.name,
                publisher: config.publisher,
                stickers: definition.slugs.map { slug in
                    StickerPreview(
                        slug: slug,
                        emojis: config.emojis[slug] ?? [],
                        previewImage: previewImage(for: slug, in: bundle),
                        accessibilityText: accessibilityText(for: slug)
                    )
                }
            )
        }

        return PackLibrary(config: config, packs: packs)
    }

    static func accessibilityText(for slug: String) -> String {
        let label = slug.replacingOccurrences(of: "-", with: " ")
        return "T Krobot, \(label)"
    }

    private static func previewImage(for slug: String, in bundle: Bundle) -> UIImage? {
        guard let url = bundle.url(
            forResource: slug,
            withExtension: "png",
            subdirectory: previewDirectory
        ) else {
            return nil
        }
        return UIImage(contentsOfFile: url.path)
    }
}
