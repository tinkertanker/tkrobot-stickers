import Messages
import UIKit

@objc(StickerBrowserViewController)
final class StickerBrowserViewController: MSStickerBrowserViewController {
    private var stickers: [MSSticker] = []

    init() {
        super.init(stickerSize: .regular)
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("init(coder:) is unused")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        loadStickers()
        stickerBrowserView.reloadData()
    }

    override func numberOfStickers(in stickerBrowserView: MSStickerBrowserView) -> Int {
        stickers.count
    }

    override func stickerBrowserView(_ stickerBrowserView: MSStickerBrowserView, stickerAt index: Int) -> MSSticker {
        stickers[index]
    }

    private func loadStickers() {
        let fileManager = FileManager.default
        var pngURLs: [URL] = []

        if let stickersFolder = Bundle.main.resourceURL?.appendingPathComponent("Stickers", isDirectory: true),
           let contents = try? fileManager.contentsOfDirectory(
            at: stickersFolder,
            includingPropertiesForKeys: [.isRegularFileKey],
            options: [.skipsHiddenFiles]
           ) {
            pngURLs.append(contentsOf: contents)
        }

        if pngURLs.isEmpty, let resourceURL = Bundle.main.resourceURL,
           let contents = try? fileManager.contentsOfDirectory(
            at: resourceURL,
            includingPropertiesForKeys: [.isRegularFileKey],
            options: [.skipsHiddenFiles]
           ) {
            pngURLs.append(contentsOf: contents)
        }

        stickers = pngURLs
            .filter { $0.pathExtension.lowercased() == "png" }
            .sorted { $0.deletingPathExtension().lastPathComponent.localizedStandardCompare($1.deletingPathExtension().lastPathComponent) == .orderedAscending }
            .compactMap { url in
                let slug = url.deletingPathExtension().lastPathComponent
                let label = slug.replacingOccurrences(of: "-", with: " ")
                return try? MSSticker(
                    contentsOfFileURL: url,
                    localizedDescription: "T Krobot, \(label)"
                )
            }
    }
}
