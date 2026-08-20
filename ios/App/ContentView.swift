import SwiftUI

struct ContentView: View {
    @Environment(\.openURL) private var openURL
    @State private var library: PackLibrary?
    @State private var loadError: String?
    @State private var alertTitle = "WhatsApp"
    @State private var alertMessage: String?

    private let columns = [GridItem(.adaptive(minimum: 72), spacing: 10)]

    var body: some View {
        NavigationStack {
            Group {
                if let library {
                    catalogue(library)
                } else if let loadError {
                    ContentUnavailableView(
                        "Catalogue unavailable",
                        systemImage: "square.stack.3d.up.slash",
                        description: Text(loadError)
                    )
                } else {
                    ProgressView("Loading stickers…")
                }
            }
            .navigationTitle("TT Stickers")
            .alert(alertTitle, isPresented: alertPresented) {
                Button("OK", role: .cancel) { alertMessage = nil }
            } message: {
                Text(alertMessage ?? "")
            }
            .onAppear(perform: loadIfNeeded)
        }
    }

    private var alertPresented: Binding<Bool> {
        Binding(
            get: { alertMessage != nil },
            set: { if !$0 { alertMessage = nil } }
        )
    }

    @ViewBuilder
    private func catalogue(_ library: PackLibrary) -> some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 28) {
                ForEach(library.packs) { pack in
                    packSection(pack)
                }

                VStack(alignment: .leading, spacing: 12) {
                    Button("Add to Telegram") {
                        openURL(library.config.telegramURL)
                    }
                    .buttonStyle(.bordered)

                    Text("Add to Telegram installs the published Telegram set, not a pack bundled in this app.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)

                    Text("iMessage stickers install with this app (Messages extension).")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .padding()
        }
    }

    @ViewBuilder
    private func packSection(_ pack: PackLibrary.Pack) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(pack.name)
                .font(.title2.weight(.semibold))

            LazyVGrid(columns: columns, spacing: 10) {
                ForEach(pack.stickers) { sticker in
                    stickerCell(sticker)
                }
            }

            Button("Add to WhatsApp") {
                addToWhatsApp(pack)
            }
            .buttonStyle(.borderedProminent)
        }
    }

    @ViewBuilder
    private func stickerCell(_ sticker: PackLibrary.StickerPreview) -> some View {
        Group {
            if let image = sticker.previewImage {
                Image(uiImage: image)
                    .resizable()
                    .scaledToFit()
            } else {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(Color.secondary.opacity(0.15))
            }
        }
        .frame(width: 72, height: 72)
        .accessibilityLabel(sticker.accessibilityText)
    }

    private func loadIfNeeded() {
        guard library == nil, loadError == nil else { return }
        do {
            let loaded = try PackLibrary.load()
            Interoperability.iOSAppStoreLink = loaded.config.iosAppStoreLink
            library = loaded
        } catch {
            loadError = error.localizedDescription
        }
    }

    private func addToWhatsApp(_ pack: PackLibrary.Pack) {
        guard Interoperability.canSend() else {
            alertTitle = "WhatsApp"
            alertMessage = "Install WhatsApp to add this sticker pack."
            return
        }

        do {
            try WhatsAppPack.send(pack)
        } catch {
            alertTitle = "WhatsApp"
            alertMessage = error.localizedDescription
        }
    }
}

#Preview {
    ContentView()
}
