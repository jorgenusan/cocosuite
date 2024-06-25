import fire

from cocotools.scripts.manipulation import coco_manipulation


def main():
    """Main entry point for the CLI."""
    fire.Fire(
        {
            "manipulation": coco_manipulation,
        }
    )


if __name__ == "__main__":
    main()
