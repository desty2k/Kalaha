import os
import argparse

from kalaha.config import __version__, __app_name__


def get_parser():
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Kalaha game",
        epilog="See 'kalaha <command> -h' for more information "
               "on a specific mode."
    )

    parser.add_argument("-V", "--version", action="version", version="v{}".format(__version__),
                        help="print version and exit")
    parser.add_argument("--log-level", default="DEBUG",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="set log level")

    subparsers = parser.add_subparsers(
        title="Available modes",
        metavar="",
        dest="mode"
    )

    # building executable
    server_parser = subparsers.add_parser(
        "server",
        aliases=["s"],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Host a game",
        description="Start a server to host a game of Kalaha."
    )

    server_parser.add_argument("-H", "--host", type=str, default="127.0.0.1",
                               help="hostname to bind to")
    server_parser.add_argument("-p", "--port", type=int, default=20202,
                               help="port to listen on")

    server_parser.add_argument("-mS", "--min-stones", type=int, default=0,
                               help="minimum amount of stones per pit")
    server_parser.add_argument("-MS", "--max-stones", type=int, default=100,
                               help="maximum amount of stones per pit")

    server_parser.add_argument("-bS", "--min-board", type=int, default=0,
                               help="minimum amount of pits per player")
    server_parser.add_argument("-BS", "--max-board", type=int, default=100,
                               help="maximum amount of pits per player")

    server_parser.add_argument("-MB", "--max-boards", type=int, default=100,
                               help="maximum amount of available boards")

    server_parser.add_argument("-tT", "--min-timeout", type=int, default=0,
                               help="minimum amount of seconds to wait for a turn")
    server_parser.add_argument("-TT", "--max-timeout", type=int, default=100,
                               help="maximum amount of seconds to wait for a turn")
    server_parser.add_argument("-r", "--remove-boards", action="store_true",
                               help="remove boards on game over")

    client_parser = subparsers.add_parser(
        "client",
        aliases=["c"],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Connect to a server",
        description="Connect to a server to play a game of Kalaha."
    )

    client_parser.add_argument("-H", "--host", type=str, default="127.0.0.1",
                               help="hostname to connect to")
    client_parser.add_argument("-p", "--port", type=int, default=20202,
                               help="port to connect to")
    client_parser.add_argument("--auto-play", "-ap", action="store_true",
                               help="start with auto-player enabled")
    client_parser.add_argument("--minimax-depth", "-md", type=int, default=4,
                               help="minimax depth")
    client_parser.add_argument("--auto-play-delay", "-apd", type=int, default=5,
                               help="delay of auto-play in seconds")
    client_parser.add_argument("--alpha-beta", "-ab", action="store_true",
                               help="enable alpha-beta pruning")
    client_parser.add_argument("--iterative-deepening", "-id", action="store_true",
                               help="enable iterative deepening")
    client_parser.add_argument("--highlight_moves", "-hm", action="store_true",
                               help="highlight pit calculated by auto-player before making move")
    return parser


def parse_args(args: list):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.mode is None:
        parser.print_help()
        return
    else:
        args.host = os.getenv("HOST", args.host)
        args.port = int(os.getenv("PORT", args.port))
        args.log_level = os.getenv("LOG_LEVEL", args.log_level)

    if args.mode == "server":
        args.min_stones = int(os.getenv("MIN_STONES", args.min_stones))
        args.max_stones = int(os.getenv("MAX_STONES", args.max_stones))
        args.min_board = int(os.getenv("MIN_BOARD", args.min_board))
        args.max_board = int(os.getenv("MAX_BOARD", args.max_board))
        args.max_boards = int(os.getenv("MAX_BOARDS", args.max_boards))
        args.min_timeout = int(os.getenv("MIN_TIMEOUT", args.min_timeout))
        args.max_timeout = int(os.getenv("MAX_TIMEOUT", args.max_timeout))
        args.remove_boards = str(os.getenv("REMOVE_BOARDS", args.remove_boards)).lower() in ("true", "1", "t")
    elif args.mode == "client":
        args.minimax_depth = int(os.getenv("MINIMAX_DEPTH", args.minimax_depth))
        args.auto_play = str(os.getenv("AUTO_PLAY", args.auto_play)).lower() in ("true", "1", "t")
        args.auto_play_delay = int(os.getenv("AUTO_PLAY_DELAY", args.auto_play_delay))
        args.alpha_beta = str(os.getenv("ALPHA_BETA", args.alpha_beta)).lower() in ("true", "1", "t")
        args.iterative_deepening = str(os.getenv("ITERATIVE_DEEPENING",
                                                 args.iterative_deepening)).lower() in ("true", "1", "t")
        args.highlight_moves = str(os.getenv("HIGHLIGHT_MOVES", args.highlight_moves)).lower() in ("true", "1", "t")
    return args
