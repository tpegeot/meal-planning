"""
Meal for a week : main function
"""

import argparse
import locale
import os
import sys
from meals_for_a_week.configuration import Configuration # noqa
from meals_for_a_week.meals_for_a_week import MealDatabase, SeasonalDatabase, MealGenerator # noqa


# Define constants
DEFAULT_CONFIG_FILE_PATH = 'database.yaml'
DEFAULT_SEASONAL_FILE_PATH = 'seasonal.yaml'
DEFAULT_HISTORY_PERIOD = 1
DEFAULT_HISTORY_FILE_PATH = 'history.yaml'


def parse_args():
    """

    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser()
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('-v', '--verbose', action="store_true")
    log_group.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('--check-config', action="store_true")
    parser.add_argument('-c', '--config', help='path to config file')
    parser.add_argument('-s', '--seasonal', default=None, help='path to seasonal file')
    parser.add_argument('-l', '--leftovers', default=None, nargs='*', help='list of leftovers')
    parser.add_argument('--veggie-meals', default=0, help='number of vegetarian meals', type=int)
    parser.add_argument('--special-meals', default=0, help='number of special meals', type=int)
    parser.add_argument('-m', '--meals', default=7, help='number of meals', type=int)
    parser.add_argument('--history-meals',
                        default=DEFAULT_HISTORY_PERIOD,
                        help='do not include meals already done over the last x weeks', type=int)
    parser.add_argument('--history', default=None, help='path to history file')
    parser.add_argument('-p', '--pretend', default=False, action="store_true")

    args = parser.parse_args()
    return args


def set_configuration(_arguments, _configuration):
    """
    Set configuration settings
    :param _arguments:
    :type _arguments:
    :param _configuration:
    :type _configuration:
    """
    if _arguments.verbose:
        _configuration.enable_verbose()
        _configuration.set_verbose_log()

    if _arguments.debug:
        _configuration.enable_debug()
        _configuration.set_debug_log()

    if _arguments.check_config:
        _configuration.enable_check_config()

    if _arguments.pretend:
        _configuration.enable_pretend_only()


def get_yaml_file(file_path, default_file_path):
    """

    :param file_path:
    :type file_path:
    :param default_file_path:
    :type default_file_path:
    :return:
    :rtype:
    """
    # Get application name
    application_name = os.path.basename(sys.argv[0])
    # Build default application dir (for ie : $HOME/.config/meals_for_a_week)
    user_config_dir = os.path.join(os.path.join(os.environ['HOME'], '.config'))
    application_dir = os.path.join(user_config_dir, application_name)
    # Default path to yaml file
    default_path_to_yaml_file = os.path.join(application_dir, default_file_path)

    if file_path:
        _database_file = file_path
    elif os.path.exists(default_path_to_yaml_file):
        _database_file = default_path_to_yaml_file
    else:
        _database_file = None
    return _database_file


def display_results(meal_planning):
    """

    :param meal_planning:
    :type meal_planning:
    """
    for meal in meal_planning.get():
        print('Plat : ' + meal.get()
              + ' (veggie : ' + str(meal.is_veggie())
              + ' ; special : ' + str(meal.is_special()) + ')')


def check_user_input(_configuration):
    """

    :return:
    :rtype:
    """
    is_meal_list_ok = False

    user_input = None
    while user_input not in ['y', 'Y', 'n', 'N', 'q', 'Q']:
        if user_input:
            _configuration.error_log('Invalid choice')
        user_input = input("Is this list of meals OK? (Y/n/q)")

    if user_input in ['y', 'Y']:
        is_meal_list_ok = True
    elif user_input in ['q', 'Q']:
        sys.exit()
    return is_meal_list_ok


def save_to_history(meal_planning, history_database):
    """
    Save generated list of meal to history file
    :param meal_planning:
    :type meal_planning:
    :param history_database:
    :type history_database:
    """
    history_database.extend(meal_planning.get())
    history_database.dump_to_yaml_file()


# This function is called with two arguments:
# the signal number and the current stack frame
def exit_gracefully(_signal_received, _frame):
    """
    Exit gracefully when CTRL+C
    :param _signal_received:
    :type _signal_received:
    :param _frame:
    :type _frame:
    """
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(1)


def main():
    """
    Main function
    """
    # Global configuration
    application_config = Configuration()

    # Argument management
    args = parse_args()

    # Define configuration
    set_configuration(args, application_config)

    database_path = get_yaml_file(args.config, DEFAULT_CONFIG_FILE_PATH)
    if not database_path:
        application_config.error_log('Cannot find config file')
        sys.exit(os.EX_NOINPUT)

    seasonal_path = get_yaml_file(args.seasonal, DEFAULT_SEASONAL_FILE_PATH)

    # Number of meals
    number_of_meals = args.meals
    number_of_veggie_meals = args.veggie_meals
    number_of_special_meals = args.special_meals

    if number_of_veggie_meals + number_of_special_meals > number_of_meals:
        application_config.error_log('You asked for too many veggie or special meals')
        sys.exit(os.EX_NOINPUT)

    # History
    number_of_history_meals = args.history_meals
    history_path = get_yaml_file(args.history, DEFAULT_HISTORY_FILE_PATH)

    # Leftovers
    if args.leftovers:
        leftovers = [leftover.lower() for leftover in args.leftovers]
        application_config.enable_leftover_mode()
        # Debug
        application_config.debug_log('List of leftovers : ' + str(leftovers))

    else:
        leftovers = None

    # Set locale to system locale
    locale.setlocale(locale.LC_ALL, '')

    # Init meal database
    database = MealDatabase(database_path, application_config)

    # Load content from yaml
    database.load()

    if seasonal_path:
        # Init seasonal database
        seasonal_database = SeasonalDatabase(seasonal_path, application_config)

        # Load content from yaml
        seasonal_database.load()

    if history_path and number_of_history_meals > 0:
        history_database = MealDatabase(history_path, application_config)
        history_database.load()
    else:
        history_database = None

    final_meal_list = False
    while not final_meal_list:

        # Build python object
        database.build()

        if seasonal_database:
            # Build python object from it
            seasonal_database.build()

        if history_database:
            history_database.build()

        # Filter database
        if seasonal_database or (history_database and number_of_history_meals > 0):
            database.filter(seasonal_database, history_database, number_of_history_meals)

        # Init meal generator
        meal_generator = MealGenerator(application_config, database.get(), number_of_meals)
        if number_of_veggie_meals > 0:
            meal_generator.set_veggie_limit(number_of_veggie_meals)
        if number_of_special_meals > 0:
            meal_generator.set_special_limit(number_of_special_meals)

        if meal_generator.is_config_valid():
            application_config.verbose_log('Config is valid')
        else:
            application_config.error_log('Config is invalid')
            sys.exit(os.EX_NOINPUT)

        meal_generator.generate(leftovers)

        meal_planning = meal_generator.get()

        display_results(meal_planning)

        if not application_config.is_pretend_only():
            final_meal_list = check_user_input(application_config)

            if final_meal_list and history_database:
                save_to_history(meal_planning, history_database)
        else:
            final_meal_list = True
