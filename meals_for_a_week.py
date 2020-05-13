#!/usr/bin/env python

import argparse
import random
import os
import datetime
import locale
import yaml

# Define constants
DEFAULT_CONFIG_FILE_PATH='config.yaml'
DEFAULT_SEASONAL_FILE_PATH='seasonal.yaml'

# Define global variable
debug = False
verbose = False
check_config_only = False

# MealCollection class
class MealCollection:
    def __init__(self):
        """
        Init MealCollection with empty __meals array
        """
        self.__meals = []

    def add(self, _meal):
        """
        Add a Meal object to __meals array
        :type _meal: object
        """
        self.__meals.append(_meal)

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
            if __meal.is_veggie() and not __meal.is_special():
                __veggie_meals.append(__meal)
        return __veggie_meals

    def get_count_veggie_meals(self):
        """

        :return:
        """
        return len(self.get_veggie_meals())

    def get_special_meals(self):
        """

        :return:
        """
        __special_meals = []
        for __meal in self.__meals:
            if __meal.is_special():
                __special_meals.append(__meal)
        return __special_meals

    def get_count_special_meals(self):
        """

        :return:
        """
        return len(self.get_special_meals())

    def get_normal_meals(self):
        """
        Get list of "normal" meals (excluding special meals but including veggie meals)
        :return:
        """
        __normal_meals = []
        for __meal in self.__meals:
            if not __meal.is_special():
                __normal_meals.append(__meal)
        return __normal_meals

    def get_random_veggie_meal(self):
        """
        Get a random meal from get_normal_meals function
        :return:
        """
        __meals = self.get_veggie_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals)-1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_special_meal(self):
        """

        :return:
        """
        __meals = self.get_special_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals)-1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_normal_meal(self):
        """

        :return:
        """
        __meals = self.get_normal_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals)-1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_meal(self):
        """

        :return:
        """
        __meals = self.get_normal_meals()
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals)-1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_count_meal(self):
        """

        :return:
        """
        return len(self.__meals)

    def remove_meal(self, _meal):
        """

        :param _meal:
        """
        self.__meals.remove(_meal)

    def restrict_by_ingredients(self, _ingredients):
        """

        :param _ingredients:
        :return:
        """
        _restricted_meal_collection = MealCollection()
        for __meal in self.__meals:
            if any(_ingredient in __meal.get_mandatory_ingredients() for _ingredient in _ingredients):
                _restricted_meal_collection.add(__meal)
        return _restricted_meal_collection


class Meal:
    def __init__(self, name):
        """

        :param name:
        """
        self.__name = name
        self.__mandatory_ingredients = []
        self.__is_special = False
        self.__is_veggie_compatible = False

    def get(self):
        return self.__name

    def is_veggie(self):
        return self.__is_veggie_compatible

    def is_special(self):
        return self.__is_special

    def set_special(self, switch):
        self.__is_special = switch

    def set_veggie(self, switch):
        self.__is_veggie_compatible = switch

    def add_mandatory_ingredients(self, _ingredient):
        self.__mandatory_ingredients.append(_ingredient)

    def get_mandatory_ingredients(self):
        return self.__mandatory_ingredients


class MealDatabase:
    def __init__(self, database_path):
        self.__database_path = database_path
        self.__database_raw_content = {}
        self.__meal_database = MealCollection()

    def get_path(self):
        return self.__database_path

    def load(self):
        try:
            __database_file = open(self.__database_path)
        except OSError as err:
            print("OS error: {0}".format(err))
            exit(os.EX_NOINPUT)
        else:
            self.__database_raw_content = yaml.load(__database_file, Loader=yaml.FullLoader)
            __database_file.close()

    def get_raw_content(self):
        return self.__database_raw_content

    def build(self, _database):
        if _database:
            _seasoning_database = _database
        else:
            _seasoning_database = None

        if "meals" in self.__database_raw_content:
            for __meal_record in self.__database_raw_content["meals"]:
                if "meal" in __meal_record:
                    seasonal = True
                    __meal = Meal(__meal_record["meal"].lower())

                    if "is_veggie_compatible" in __meal_record:
                        __meal.set_veggie(True)

                    if "is_special" in __meal_record:
                        __meal.set_special(True)

                    if "mandatory_ingredients" in __meal_record:
                        for _mandatory_ingredient in __meal_record["mandatory_ingredients"]:
                            __meal.add_mandatory_ingredients(_mandatory_ingredient.lower())

                            if _seasoning_database and \
                                _mandatory_ingredient.lower() in _seasoning_database.get_restricted_vegetables() and \
                                    _mandatory_ingredient.lower() not in _seasoning_database.get_current_vegetables():
                                seasonal = False

                    # If seasoning database exists and all ingredients are seasonal,
                    # then meal is add to the db
                    if _seasoning_database and seasonal:
                        self.__meal_database.add(__meal)
                    # If seasoning database doesn't, the meal is add to the db
                    elif not _seasoning_database:
                        self.__meal_database.add(__meal)

    def get(self):
        return self.__meal_database


class MonthlyVegetables:
    def __init__(self, name):
        self.__name = name
        self.__vegetables = []

    def add(self, _vegetable_name):
        self.__vegetables.append(_vegetable_name)

    def get(self):
        return self.__name

    def get_vegetables(self):
        return self.__vegetables


class SeasonalDatabase:
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
        """
        return self.__database_path

    def load(self):
        try:
            __database_file = open(self.__database_path)
        except OSError as err:
            print("OS error: {0}".format(err))
            exit(os.EX_NOINPUT)
        else:
            self.__database_raw_content = yaml.load(__database_file, Loader=yaml.FullLoader)
            __database_file.close()

    def get_raw_content(self):
        return self.__database_raw_content

    def build(self):
        if "months" in self.__database_raw_content:
            for __month_record in self.__database_raw_content["months"]:
                if "month" in __month_record:
                    __month = MonthlyVegetables(__month_record["month"].lower())
                    self.__database.append(__month)
                    if "vegetables" in __month_record:
                        for __vegetable in __month_record["vegetables"]:
                            __month.add(__vegetable.lower())

    def get(self):
        return self.__database

    def get_restricted_vegetables(self):
        _get_restricted_vegetables = []
        for _month in self.__database:
            _get_restricted_vegetables.extend(_month.get_vegetables())
        return _get_restricted_vegetables

    def get_current_month(self):
        __current_month_name = datetime.datetime.today().strftime('%B').lower()
        __current_month = None
        for _month in self.__database:
            if __current_month_name == _month.get():
                __current_month = _month
        return __current_month

    def get_current_vegetables(self):
        return self.get_current_month().get_vegetables()


class MealGenerator:
    def __init__(self, _meal_database, meal_limit):
        self.__meal_database = _meal_database
        self.__meal_limit = meal_limit
        self.__meal_veggie_limit = 0
        self.__meal_special_limit = 0
        self.__meal_collection = MealCollection()

    def get(self):
        return self.__meal_collection

    def generate(self, _leftovers):
        # If the list of meals must be generated from leftovers,
        # then build a list of potential compatible meals
        if _leftovers:
            _restricted_database = self.__meal_database.restrict_by_ingredients(_leftovers)
        else:
            _restricted_database = None

        # First look for vegetarian meals
        while self.__meal_collection.get_count_veggie_meals() < self.__meal_veggie_limit:
            __meal = None

            # If a list of leftover-compatible meals is available
            if _restricted_database and _restricted_database.get_count_meal() > 0:
                # Then try to get a random meal from it
                __meal = _restricted_database.get_random_veggie_meal()
                # If a veggie meal was found in the list of leftover-compatible meals
                if __meal:
                    # Remove meal from list of potential meals
                    _restricted_database.remove_meal(__meal)

            # If meal is empty (either no leftover or no compatible meal found before)
            if not __meal:
                # Then get a random meal
                __meal = self.__meal_database.get_random_veggie_meal()

            # If a meal was found and this meal is already part of the list
            if __meal and __meal not in self.__meal_collection.get():
                # Add it to the meal collection
                self.__meal_collection.add(__meal)

                # Remove meal from list of potential meals
                self.__meal_database.remove_meal(__meal)

        # Then look for "special" meals
        while self.__meal_collection.get_count_special_meals() < self.__meal_special_limit:
            __meal = None

            # If a list of leftover-compatible meals is available
            if _restricted_database and _restricted_database.get_count_meal() > 0:
                # Then try to get a random meal from it
                __meal = _restricted_database.get_random_special_meal()
                if __meal:
                    # Remove meal from list of potential meals
                    _restricted_database.remove_meal(__meal)

            # If meal is empty (either no leftover or no compatible meal found before)
            if not __meal:
                # Then get a random meal
                __meal = self.__meal_database.get_random_special_meal()

            # If a meal was found and this meal is already part of the list
            if __meal and __meal not in self.__meal_collection.get():
                # Add it to the meal collection
                self.__meal_collection.add(__meal)

                # Remove meal from list of potential meals
                self.__meal_database.remove_meal(__meal)

        # Finally get remaining meals
        while self.__meal_collection.get_count_meal() < self.__meal_limit:
            __meal = None

            # If a list of leftover-compatible meals is available
            if _restricted_database and _restricted_database.get_count_meal() > 0:
                # Then try to get a random meal from it
                __meal = _restricted_database.get_random_normal_meal()
                if __meal:
                    # Then get a random meal
                    _restricted_database.remove_meal(__meal)

            # If meal is empty (either no leftover or no compatible meal found before)
            if not __meal:
                # Remove meal from list of potential meals
                __meal = self.__meal_database.get_random_normal_meal()

            # If a meal was found and this meal is already part of the list
            if __meal and __meal not in self.__meal_collection.get():
                # Add it to the meal collection
                self.__meal_collection.add(__meal)

                # Remove meal from list of potential meals
                self.__meal_database.remove_meal(__meal)

    # Set the number of vegetarian meals we want
    def set_veggie_limit(self, veggie_limit):
        self.__meal_veggie_limit = veggie_limit

    # Set the number of special meals we want
    def set_special_limit(self, special_limit):
        self.__meal_special_limit = special_limit


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('--check-config', action="store_true")
    parser.add_argument('-c', '--config', help='path to config file')
    parser.add_argument('-s','--seasonal', help='path to seasonal file')
    parser.add_argument('-l', '--leftovers', nargs='*', help='list of letfovers')
    #parser.add_argument('--veggie-meals', help='number of vegetarian meals', int)
    #parser.add_argument('--special-meals', help='number of special meals', int)
    #parser.add_argument('-n','--meals', help='list of letfovers', int)
    #parser.add_argument('--history', help='don't include meals offered over the last x weeks', int)
    args = parser.parse_args()
    return args


def main():
    """
    Main function
    TODO : add argument management
    """
    args = parse_args()

    if args.verbose:
        verbose = True

    if args.debug:
        debug = True

    if args.check_config:
        check_config_only = True

    # Set locale to system locale
    locale.setlocale(locale.LC_ALL, '')

    # Init meal database
    if args.config:
        database = MealDatabase(args.config)
    else :
        database = MealDatabase(DEFAULT_CONFIG_FILE_PATH)
    # Load content from yaml
    database.load()

    # Init seasonal database
    if args.seasonal:
        seasonal_database = SeasonalDatabase('seasonal.yaml')
    else:
        seasonal_database = SeasonalDatabase(DEFAULT_SEASONAL_FILE_PATH)
    # Load content from yaml
    seasonal_database.load()
    # Build python object from it
    seasonal_database.build()

    if seasonal_database:
        database.build(seasonal_database)
    else:
        database.build(None)

    # Init meal generator
    meal_generator = MealGenerator(database.get(), 7)
    meal_generator.set_veggie_limit(2)
    meal_generator.set_special_limit(2)

    if args.leftovers:
        leftovers = [leftover.lower() for leftover in args.leftovers]
        meal_generator.generate(leftovers)
    else:
        meal_generator.generate(None)

    meal_planning = meal_generator.get()

    for meal in meal_planning.get():
        print('Plat : ' + meal.get() \
            + ' (veggie : ' + str(meal.is_veggie()) \
            + ' ; special : ' + str(meal.is_special()) + ')')


if __name__ == "__main__":
    main()
