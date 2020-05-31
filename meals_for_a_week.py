#!/usr/bin/env python

"""
Meal for a week
"""

import argparse
import random
import os
import datetime
import locale
import sys
import yaml


# Define constants
DEFAULT_CONFIG_FILE_PATH = 'config.yaml'
DEFAULT_SEASONAL_FILE_PATH = 'seasonal.yaml'


# Configuration class
class Configuration:
    """
    Configuration class
    """
    def __init__(self):
        """
        Init configuration class
        """
        self._debug = False
        self._verbose = False
        self._check_config = False
        # Order matters in _meal_type
        self._meal_types = ['VEGGIE', 'SPECIAL', 'NORMAL']

    def enable_verbose(self):
        """
        Enable verbose mode
        """
        self._verbose = True

    def enable_debug(self):
        """
        Enable debug mode
        """
        self._debug = True

    def enable_check_config(self):
        """
        Enable check config mode only
        """
        self._check_config = True

    def is_verbose(self):
        """
        Return if verbose mode is enable
        :return:
        :rtype:
        """
        return self._verbose

    def is_debug(self):
        """
        Return if debug mode is enable
        :return:
        :rtype:
        """
        return self._debug

    def get_meal_types(self):
        """

        :return:
        :rtype:
        """
        return self._meal_types


# MealCollection class
class MealCollection:
    """
    Meal class
    """
    def __init__(self, configuration):
        """
        Init MealCollection with empty __meals array
        """
        self.__meals = []
        self._configuration = configuration

    def add(self, _meal):
        """
        Add a Meal object to __meals array
        :type _meal: object
        """
        self.__meals.append(_meal)

    def remove_meal(self, _meal):
        """

        :param _meal:
        """
        self.__meals.remove(_meal)

    # Get functions #

    def get(self):
        """

        :return:
        """
        return self.__meals

    def get_veggie_meals(self):
        """

        :return:
        """
        __veggie_meals = []
        for __meal in self.__meals:
            if __meal.is_veggie() \
                    and not __meal.is_special() \
                    and __meal.is_enable():
                __veggie_meals.append(__meal)
        return __veggie_meals

    def get_special_meals(self):
        """

        :return:
        """
        __special_meals = []
        for __meal in self.__meals:
            if __meal.is_special() and __meal.is_enable():
                __special_meals.append(__meal)
        return __special_meals

    def get_normal_meals(self):
        """
        Get list of "normal" meals (excluding special meals but including veggie meals)
        :return:
        """
        __normal_meals = []
        for __meal in self.__meals:
            if not __meal.is_special() and __meal.is_enable():
                __normal_meals.append(__meal)
        return __normal_meals

    def get_meals(self):
        """
        Get list of "normal" meals (excluding special meals but including veggie meals)
        :return:
        """
        __meals = []
        for __meal in self.__meals:
            __meals.append(__meal.get())
        return __meals

    # Random functions #
    def get_random_veggie_meal(self):
        """
        Get a random meal from get_normal_meals function
        :return:
        """
        __meals = self.get_veggie_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals) - 1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_special_meal(self):
        """

        :return:
        """
        __meals = self.get_special_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals) - 1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_normal_meal(self):
        """

        :return:
        """
        __meals = self.get_normal_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals) - 1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_meal(self):
        """

        :return:
        """
        __meals = self.get_normal_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals) - 1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_meal_by_type(self, _meal_type):
        """

        :param _meal_type:
        :type _meal_type:
        :return:
        :rtype:
        """
        if _meal_type not in self._configuration:
            sys.exit(os.EX_SOFTWARE)
        _meal = None
        if _meal_type == 'NORMAL':
            _meal = self.get_random_normal_meal()
        elif _meal_type == 'VEGGIE':
            _meal = self.get_random_veggie_meal()
        elif _meal_type == 'SPECIAL':
            _meal = self.get_random_special_meal()
        return _meal

    # Count functions #
    def get_count_veggie_meals(self):
        """

        :return:
        """
        return len(self.get_veggie_meals())

    def get_count_special_meals(self):
        """

        :return:
        """
        return len(self.get_special_meals())

    def get_count_meal(self):
        """

        :return:
        """
        return len(self.__meals)

    def get_count_by_meal_type(self, _meal_type):
        """

        :param _meal_type:
        :type _meal_type:
        :return:
        :rtype:
        """
        if _meal_type not in self._configuration:
            sys.exit(os.EX_SOFTWARE)
        _count = 0
        if _meal_type == 'NORMAL':
            _count = self.get_count_meal()
        elif _meal_type == 'VEGGIE':
            _count = self.get_count_veggie_meals()
        elif _meal_type == 'SPECIAL':
            _count = self.get_count_special_meals()

        return _count

    # Misc functions #

    def restrict_by_ingredients(self, _ingredients):
        """

        :param _ingredients:
        :return:
        """
        _restricted_meal_collection = MealCollection(self._configuration)
        for __meal in self.__meals:
            if any(_ingredient in __meal.get_mandatory_ingredients()
                   for _ingredient in _ingredients):
                _restricted_meal_collection.add(__meal)
        return _restricted_meal_collection


class Meal:
    """
    Meal class
    """
    def __init__(self, name):
        """

        :param name:
        """
        self.__name = name
        self.__mandatory_ingredients = []
        self.__is_special = False
        self.__is_veggie_compatible = False
        self.__is_enable = True

    def get(self):
        """

        :return:
        :rtype:
        """
        return self.__name

    def is_veggie(self):
        """

        :return:
        :rtype:
        """
        return self.__is_veggie_compatible

    def is_special(self):
        """

        :return:
        :rtype:
        """
        return self.__is_special

    def is_enable(self):
        """
        :return:
        :rtype: object
        """
        return self.__is_enable

    def set_special(self, switch):
        """

        :param switch:
        :type switch:
        """
        self.__is_special = switch

    def set_veggie(self, switch):
        """

        :param switch:
        :type switch:
        """
        self.__is_veggie_compatible = switch

    def disable(self):
        """
        Disable menu
        """
        self.__is_enable = False

    def add_mandatory_ingredients(self, _ingredient):
        """

        :param _ingredient:
        :type _ingredient:
        """
        self.__mandatory_ingredients.append(_ingredient)

    def get_mandatory_ingredients(self):
        """

        :return:
        :rtype:
        """
        return self.__mandatory_ingredients


class MealDatabase:
    """
    MealDatabase class
    """
    def __init__(self, database_path, configuration):
        """

        :param database_path:
        :type database_path:
        """
        self.__database_path = database_path
        self.__database_raw_content = {}
        self._configuration = configuration
        self.__meal_database = MealCollection(self._configuration)

    def get_path(self):
        """

        :return:
        :rtype:
        """
        return self.__database_path

    def load(self):
        """
        Load function
        """
        try:
            __database_file = open(self.__database_path)
        except OSError as err:
            print("OS error: {0}".format(err))
            sys.exit(os.EX_OSFILE)
        else:
            self.__database_raw_content = yaml.load(__database_file, Loader=yaml.FullLoader)
            __database_file.close()

    def get_raw_content(self):
        """

        :return:
        :rtype:
        """
        return self.__database_raw_content

    def build(self):
        """
        Build meal database
        """

        if "meals" in self.__database_raw_content:
            for __meal_record in self.__database_raw_content["meals"]:
                if "meal" in __meal_record:
                    __meal = Meal(__meal_record["meal"].lower())

                    if "is_veggie_compatible" in __meal_record:
                        __meal.set_veggie(True)

                    if "is_special" in __meal_record:
                        __meal.set_special(True)

                    if "mandatory_ingredients" in __meal_record:
                        for _mandatory_ingredient in __meal_record["mandatory_ingredients"]:
                            __meal.add_mandatory_ingredients(_mandatory_ingredient.lower())

                    self.__meal_database.add(__meal)

    def get(self):
        """

        :return:
        :rtype:
        """
        return self.__meal_database

    def filter(self, _seasoning, _history):
        """
        Filter database
        :param _seasoning:
        :type _seasoning:
        :param _history:
        :type _history:
        """
        if _seasoning:
            for _meal in self.get().get():
                _meal_ingredients = _meal.get_mandatory_ingredients()
                for _meal_ingredient in _meal_ingredients:
                    if _meal_ingredient.lower() in _seasoning.get_restricted_vegetables() and \
                            _meal_ingredient.lower() not in _seasoning.get_current_vegetables():
                        _meal.disable()

        if _history:
            for _meal in self.get().get():
                if _meal.get()  in _history.get().get_meals():
                    _meal.disable()


class MonthlyVegetables:
    """
    MonthlyVegetables class
    """
    def __init__(self, name):
        """

        :param name:
        :type name:
        """
        self.__name = name
        self.__vegetables = []

    def add(self, _vegetable_name):
        """

        :param _vegetable_name:
        :type _vegetable_name:
        """
        self.__vegetables.append(_vegetable_name)

    def get(self):
        """

        :return:
        :rtype:
        """
        return self.__name

    def get_vegetables(self):
        """

        :return:
        :rtype:
        """
        return self.__vegetables


class SeasonalDatabase:
    """
    SeasonalDatabase class
    """
    def __init__(self, database_path):
        """

        :param database_path:
        """
        self.__database_path = database_path
        self.__database_raw_content = {}
        self.__database = []

    def get_path(self):
        """

        :return:
        :rtype:
        """
        return self.__database_path

    def load(self):
        """
        Load function
        """
        try:
            __database_file = open(self.__database_path)
        except OSError as err:
            print("OS error: {0}".format(err))
            sys.exit(os.EX_OSFILE)
        else:
            self.__database_raw_content = yaml.load(__database_file, Loader=yaml.FullLoader)
            __database_file.close()

    def get_raw_content(self):
        """

        :return:
        :rtype:
        """
        return self.__database_raw_content

    def build(self):
        """
        Build function
        """
        if "months" in self.__database_raw_content:
            for __month_record in self.__database_raw_content["months"]:
                if "month" in __month_record:
                    __month = MonthlyVegetables(__month_record["month"].lower())
                    self.__database.append(__month)
                    if "vegetables" in __month_record:
                        for __vegetable in __month_record["vegetables"]:
                            __month.add(__vegetable.lower())

    def get(self):
        """

        :return:
        :rtype:
        """
        return self.__database

    def get_restricted_vegetables(self):
        """

        :return:
        :rtype:
        """
        _get_restricted_vegetables = []
        for _month in self.__database:
            _get_restricted_vegetables.extend(_month.get_vegetables())
        return _get_restricted_vegetables

    def get_current_month(self):
        """

        :return:
        :rtype:
        """
        __current_month_name = datetime.datetime.today().strftime('%B').lower()
        __current_month = None
        for _month in self.__database:
            if __current_month_name == _month.get():
                __current_month = _month
        return __current_month

    def get_current_vegetables(self):
        """

        :return:
        :rtype:
        """
        return self.get_current_month().get_vegetables()


class MealGenerator:
    """
    MealGenerator class
    """

    def __init__(self, configuration, meal_database, meal_limit):
        """

        :param _meal_database:
        :type _meal_database:
        :param meal_limit:
        :type meal_limit:
        """
        self._configuration = configuration
        self._meal_database = meal_database
        self._meal_limit = meal_limit
        self._meal_veggie_limit = 0
        self._meal_special_limit = 0
        self._meal_collection = MealCollection(self._configuration)

    def get(self):
        """

        :return:
        :rtype:
        """
        return self._meal_collection

    def is_config_valid(self):
        """

        :return:
        :rtype:
        """
        _check = True
        if self._meal_limit > self._meal_database.get_count_meal():
            _check = False

        if self._meal_veggie_limit > self._meal_database.get_count_veggie_meals():
            _check = False

        if self._meal_special_limit > self._meal_database.get_count_special_meals():
            _check = False

        if self._meal_veggie_limit + self._meal_special_limit \
                > self._meal_database.get_count_meal():
            _check = False

        return _check

    def get_meal_limit_by_type(self, _meal_type):
        """

        :return:
        :rtype:
        """
        if _meal_type not in self._configuration:
            sys.exit(os.EX_SOFTWARE)
        _meal_limit = 0
        if _meal_type == 'NORMAL':
            _meal_limit = self._meal_limit
        elif _meal_type == 'VEGGIE':
            _meal_limit = self._meal_veggie_limit
        elif _meal_type == 'SPECIAL':
            _meal_limit = self._meal_special_limit
        return _meal_limit

    # Generate random meal list according to various conditions
    def generate_meal_by_type(self, _restricted_database, _meal_type):
        """

        :param _restricted_database:
        :type _restricted_database:
        :param _meal_type:
        :type _meal_type:
        """
        _meal_limit = self.get_meal_limit_by_type(_meal_type)

        while self._meal_collection.get_count_by_meal_type(_meal_type) < _meal_limit:
            _meal = None

            # If a list of leftover-compatible meals is available
            if _restricted_database and _restricted_database.get_count_meal() > 0:
                # Then try to get a random meal from it
                _meal = _restricted_database.get_random_meal_by_type(_meal_type)

                # If a veggie meal was found in the list of leftover-compatible meals
                if _meal:
                    # Remove meal from list of potential meals
                    _restricted_database.remove_meal(_meal)

            # If meal is empty (either no leftover or no compatible meal found before)
            if not _meal:
                # Then get a random meal
                _meal = self._meal_database.get_random_meal_by_type(_meal_type)

            # If a meal was found and this meal is not already part of the list
            if _meal and _meal not in self._meal_collection.get():
                # Add it to the meal collection
                self._meal_collection.add(_meal)

                # Remove meal from list of potential meals
                self._meal_database.remove_meal(_meal)

            if self._configuration.is_debug():
                print('DEBUG : ' + _meal.get() + ' (' + _meal_type + ')')

    def generate(self, _leftovers):
        """

        :param _leftovers:
        :type _leftovers:
        """
        # If the list of meals must be generated from leftovers,
        # then build a list of potential compatible meals
        if _leftovers:
            _restricted_database = self._meal_database.restrict_by_ingredients(_leftovers)
        else:
            _restricted_database = None

        for _meal_type in self._configuration.get_meal_types():
            self.generate_meal_by_type(_restricted_database, _meal_type)

    # Set the number of vegetarian meals we want
    def set_veggie_limit(self, veggie_limit):
        """

        :param veggie_limit:
        :type veggie_limit:
        """
        self._meal_veggie_limit = veggie_limit

    # Set the number of special meals we want
    def set_special_limit(self, special_limit):
        """

        :param special_limit:
        :type special_limit:
        """
        self._meal_special_limit = special_limit


def parse_args():
    """

    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('--check-config', action="store_true")
    parser.add_argument('-c', '--config', help='path to config file')
    parser.add_argument('-s', '--seasonal', default=None, help='path to seasonal file')
    parser.add_argument('-l', '--leftovers', default=None, nargs='*', help='list of leftovers')
    parser.add_argument('--veggie-meals', default=0, help='number of vegetarian meals', type=int)
    parser.add_argument('--special-meals', default=0, help='number of special meals', type=int)
    parser.add_argument('-m', '--meals', default=7, help='number of meals', type=int)
    parser.add_argument('--history-meals',
                        default=0,
                        help='do not include meals already done over the last x weeks', type=int)
    parser.add_argument('--history', default=None, help='path to history file')

    args = parser.parse_args()
    return args


def get_yaml_file(file_path, default_file_path):
    """

    :param file_path:
    :type file_path:
    :param default_file_path:
    :type default_file_path:
    :return:
    :rtype:
    """
    if file_path:
        _database_file = file_path.config
    elif os.path.exists(default_file_path):
        _database_file = default_file_path
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


def main():
    """
    Main function
    """
    # Global configuration
    configuration = Configuration()

    # Argument management
    args = parse_args()

    if args.verbose:
        configuration.enable_verbose()

    if args.debug:
        configuration.enable_debug()

    if args.check_config:
        configuration.enable_check_config()

    database_path = get_yaml_file(args.config, DEFAULT_CONFIG_FILE_PATH)
    if not database_path:
        sys.exit(os.EX_NOINPUT)

    seasonal_path = get_yaml_file(args.seasonal, DEFAULT_SEASONAL_FILE_PATH)

    # Number of meals
    number_of_meals = args.meals
    number_of_veggie_meals = args.veggie_meals
    number_of_special_meals = args.special_meals

    if number_of_veggie_meals + number_of_special_meals > number_of_meals:
        sys.exit(os.EX_NOINPUT)

    # History
    number_of_history_meals = args.history_meals
    history_path = args.history

    # Leftovers
    if args.leftovers:
        leftovers = [leftover.lower() for leftover in args.leftovers]
    else:
        leftovers = None

    # Set locale to system locale
    locale.setlocale(locale.LC_ALL, '')

    # Init meal database
    database = MealDatabase(database_path, configuration)

    # Load content from yaml
    database.load()

    if seasonal_path:
        # Init seasonal database
        seasonal_database = SeasonalDatabase(seasonal_path)

        # Load content from yaml
        seasonal_database.load()

        # Build python object from it
        seasonal_database.build()

    if history_path and number_of_history_meals > 0:
        history_database = MealDatabase(history_path, configuration)
        history_database.load()
        history_database.build()
    else:
        history_database = None

    # Build python object
    database.build()

    # Filter database
    database.filter(seasonal_database, history_database)

    # Init meal generator
    meal_generator = MealGenerator(configuration, database.get(), number_of_meals)
    if number_of_veggie_meals > 0:
        meal_generator.set_veggie_limit(number_of_veggie_meals)
    if number_of_special_meals > 0:
        meal_generator.set_special_limit(number_of_special_meals)

    if meal_generator.is_config_valid():
        if configuration.is_verbose():
            print('Config valid')
    else:
        sys.exit(os.EX_NOINPUT)

    meal_generator.generate(leftovers)

    meal_planning = meal_generator.get()

    display_results(meal_planning)


if __name__ == "__main__":
    main()
