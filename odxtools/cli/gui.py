import argparse

_odxtools_tool_name_ = "gui"

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "gui",
        description="Launch the odxtools graphical user interface.",
        help="Launch the odxtools graphical user interface.",
    )


def run(args):
    from odxtools.gui import main
    main.main()
