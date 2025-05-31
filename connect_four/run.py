from connect_four.tournament import main

if __name__ == "__main__":
    import logging

    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler("connect_four.log", mode='a')
    file_formatter = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    main()

