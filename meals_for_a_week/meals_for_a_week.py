"""
Meal for a week : classes related to Meals and databases
"""
import datetime
import os
import random
import sys
import yaml


# MealCollection class
class MealCollection:
    """
    Meal class
    """
    def __init__(self, _configuration):
        """
        Init MealCollection with empty __meals array
        """
        self.__meals = []
        self._configuration = _configuration

    def add(self, _meal):
        """
        Add a Meal object to __meals array
        :type _meal: object
        """
        self.__meals.append(_meal)

    def extend(self, _meals):
        """
        Extend meals array with another __meals array
        :param _meals:
        :type _meals:
        :type _meal: object
        """
        self.__meals.extend(_meals)

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

    def get_normal_meals(self, strict_mode):
        """
        Get list of "normal" meals
        - if strict mode : excluding special meals but including veggie meals
        - if not strict mode (when leftovers) : including special meals AND veggie meals
        :type strict_mode
        :return:
        """
        __normal_meals = []
        for __meal in self.__meals:
            if __meal.is_enable():
                if strict_mode and not __meal.is_special():
                    __normal_meals.append(__meal)
                elif not strict_mode:
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
        if self._configuration.is_leftover_mode():
            __meals = self.get_normal_meals(False)
        else:
            __meals = self.get_normal_meals(True)
        __random_meal = None

        if __meals:
            __random_int = random.randint(0, len(__meals) - 1)
            __random_meal = __meals[__random_int]

        return __random_meal

    def get_random_meal(self):
        """

        :return:
        """
        __meals = self.get_normal_meals(False)
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
        if _meal_type not in self._configuration.get_meal_types():
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
        if _meal_type not in self._configuration.get_meal_types():
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
        # Get shuffled / randomized meal list
        for __meal in random.sample(self.__meals, len(self.__meals)):
            _meal_ingredients = __meal.get_mandatory_ingredients()

            # Check if any ingredient in current meal is available in leftovers
            if any(_ingredient in _meal_ingredients
                   for _ingredient in _ingredients):
                # Enable meal irrespective of seasoning and history meals
                # We want to use leftovers in any case
                if not __meal.is_enable():
                    __meal.enable()

                # Add meal to restricted collection
                _restricted_meal_collection.add(__meal)

                # Remove ingredients used in current meal from leftovers
                _ingredients = [_ingredient for _ingredient in _ingredients
                                if _ingredient not in _meal_ingredients]

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

    def enable(self):
        """
        Enable meal manually
        """
        self.__is_enable = True

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
    def __init__(self, database_path, _configuration):
        """

        :param database_path:
        :type database_path:
        """
        self.__database_path = database_path
        self.__database_raw_content = {}
        self._configuration = _configuration
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
            self._configuration.error_log('OS error: {0}'.format(err))
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

    def filter(self, _seasoning, _history, _number_of_history_meals):
        """
        Filter database
        :param _number_of_history_meals:
        :type _number_of_history_meals:
        :param _seasoning:
        :type _seasoning:
        :param _history:
        :type _history:
        """
        if _seasoning:
            for _meal in self.__meal_database.get():
                _meal_ingredients = _meal.get_mandatory_ingredients()
                for _meal_ingredient in _meal_ingredients:
                    if _meal_ingredient.lower() in _seasoning.get_restricted_vegetables() and \
                            _meal_ingredient.lower() not in _seasoning.get_current_vegetables():
                        _meal.disable()

        if _history:
            history_meals = _history.get().get_meals()[-_number_of_history_meals*7:]
            self._configuration.debug_log('Meals from history database: ' + str(history_meals))

            for _meal in self.__meal_database.get():
                # Disable meal which was part of history file over the
                # last _number_of_history_meals weeks * 7 days
                if _meal.get() in history_meals:
                    _meal.disable()

    def extend(self, another_meal_collection):
        """

        :param another_meal_collection:
        :type another_meal_collection:
        """
        self.__meal_database.extend(another_meal_collection)

    def dump_to_yaml_file(self):
        """
        Dump database to yaml file
        """
        meal_list = []
        for meal in self.__meal_database.get():
            meal_list.append({'meal': str(meal.get())})
        yaml_data = {'meals': meal_list}

        try:
            __database_file = open(self.__database_path, 'w')
        except OSError as err:
            self._configuration.error_log('OS error: {0}'.format(err))
            sys.exit(os.EX_OSFILE)
        else:
            yaml.dump(yaml_data, __database_file, allow_unicode=True)
            __database_file.close()


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
    def __init__(self, database_path, _configuration):
        """

        :param database_path:
        """
        self.__database_path = database_path
        self.__database_raw_content = {}
        self.__database = []
        self._configuration = _configuration

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
            self._configuration.error_log('OS error: {0}'.format(err))
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

    def __init__(self, _configuration, meal_database, meal_limit):
        """

        :param meal_database:
        :type meal_database:
        :param meal_limit:
        :type meal_limit:
        """
        self._configuration = _configuration
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
        if _meal_type not in self._configuration.get_meal_types():
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

        # Debug
        self._configuration.debug_log('For ' + _meal_type
                                      + ' type, generate '
                                      + str(_meal_limit) + ' meal(s)')
        while self._meal_collection.get_count_by_meal_type(_meal_type) < _meal_limit:
            _meal = None

            # If a list of leftover-compatible meals is available
            if _restricted_database and _restricted_database.get_count_meal() > 0:
                # Debug
                self._configuration.debug_log('Trying to find a '
                                              + _meal_type + ' meal to use leftovers')

                # Then try to get a random meal from it
                _meal = _restricted_database.get_random_meal_by_type(_meal_type)
                # If a meal was found in the list of leftover-compatible meals
                if _meal:
                    # Debug
                    self._configuration.debug_log('Found a leftover-compatible meal : '
                                                  + _meal.get())

                    # Remove meal from list of potential meals
                    _restricted_database.remove_meal(_meal)

            # If meal is empty (either no leftover or no compatible meal found before)
            if not _meal:
                # Then get a random meal
                # Debug
                self._configuration.debug_log('Tring to find a ' + _meal_type + ' meal')
                _meal = self._meal_database.get_random_meal_by_type(_meal_type)

            # If a meal was found and this meal is not already part of the list
            if _meal and _meal not in self._meal_collection.get():
                # Add it to the meal collection
                self._meal_collection.add(_meal)

                # Remove meal from list of potential meals
                self._meal_database.remove_meal(_meal)

                # Debug
                self._configuration.debug_log('Found a meal : ' + _meal.get())

    def generate(self, _leftovers):
        """

        :param _leftovers:
        :type _leftovers:
        """
        # If the list of meals must be generated from leftovers,
        # then build a list of potential compatible meals
        if _leftovers:
            _restricted_database = self._meal_database.restrict_by_ingredients(_leftovers)
            # Debug
            self._configuration.debug_log('List of meal(s) compatible with leftovers : ' +
                                          str(_restricted_database.get_meals()))
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
