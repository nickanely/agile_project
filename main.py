from content_loader import QuoteLoader, ImageLoader
from send_to_teams import TeamsNotifier


def main():
    quote_loader = QuoteLoader()
    image_loader = ImageLoader()

    notifier = TeamsNotifier(quote_loader, image_loader)

    notifier.action()


if __name__ == "__main__":
    main()
