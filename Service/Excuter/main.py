import hwinfo

if __name__ == '__main__':
    with open('logging.json', 'rt') as f:
        config = json.load(f)

    logging.config.dictConfig(config)

    logger = logging.getLogger()
    logger.info("test!!!")