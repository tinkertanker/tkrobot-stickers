import Messages
import UIKit

@objc(MessagesViewController)
final class MessagesViewController: MSMessagesAppViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let browser = StickerBrowserViewController()
        addChild(browser)
        browser.view.frame = view.bounds
        browser.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(browser.view)
        browser.didMove(toParent: self)
    }
}
