class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.trainig_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.trainig_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_OUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 1.79

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                 + self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_OUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    METERS_TO_SECONDS_COEFFICIENT: float = 0.278
    CENTEMETERS_TO_METERS: int = 100

    def __init__(self, action, duration, weight,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.weight
                + ((self.get_mean_speed()
                    * self.METERS_TO_SECONDS_COEFFICIENT)**2
                    / (self.height / self.CENTEMETERS_TO_METERS))
                * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.MIN_IN_OUR)

    # def get_spent_calories(self) -> float:
    #     mean_speed = (self.get_mean_speed()
    #                   * self.METERS_TO_SECONDS_COEFFICIENT)
    #     self.height /= self.CENTEMETERS_TO_METERS
    #     return ((self.COEFF_CALORIE_1 * self.weight + (mean_speed**2
    #             / self.height) * self.COEFF_CALORIE_2
    #              * self.weight) * self.duration * self.MIN_IN_OUR)


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight * self.duration)

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP) / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking,
                                                }

    if workout_type in type_training:
        return type_training[workout_type](*data)
    else:
        raise ValueError(f'Неизвестный тип тренировки {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()

    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
