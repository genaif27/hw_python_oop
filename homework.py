from __future__ import annotations


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    training_type: str = 'Бег'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_1 * self.get_mean_speed() -
                self.coeff_calorie_2)*self.weight/self.M_IN_KM*self.duration*60


"""Тренировка: бег."""


class SportsWalking(Training):
    coeff_walking_1: float = 0.035
    coeff_walking_2: float = 0.029
    training_type: str = 'Ходьба'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.coef_walking_2 = 0.029
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.coeff_walking_1 * self.weight + (
                self.get_mean_speed() ** 2 // self.height)
                * self.coef_walking_2 * self.weight) * (self.duration * 60)


'Тренировка: спортивная ходьба.'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    swim_cal_coef_1: float = 1.1
    swim_coef: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool*self.count_pool/self.M_IN_KM/self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() +
                self.swim_cal_coef_1) * self.swim_coef * self.weight)


def read_package(
                workout_type: str,
                data: list
                ) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_classes = {
                            'SWM': Swimming,
                            'RUN': Running,
                            'WLK': SportsWalking,
                            }
    if workout_type not in workout_type_classes:
        allowed = ', '.join(workout_type_classes)
        raise ValueError(
            f'Неизвестный тип тренировки: "{workout_type}".'
            f' Допустимые значения: "{allowed}".'
                        )
    return workout_type_classes[workout_type](*data)


def main(training: Training):
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        trainingObject = read_package(workout_type, data)
        main(trainingObject)
