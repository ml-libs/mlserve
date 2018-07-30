from mlserve.main import main, cli_parser


if __name__ == '__main__':
    args = cli_parser()
    main(args.host, args.port, args.config, workers=args.workers)
