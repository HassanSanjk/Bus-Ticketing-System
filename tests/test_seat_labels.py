import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from views import generate_seat_labels


def test_generate_4_seats():
    seats = generate_seat_labels(4)
    assert seats == ["A1", "A2", "A3", "A4"]


def test_generate_5_seats():
    seats = generate_seat_labels(5)
    assert seats == ["A1", "A2", "A3", "A4", "B1"]


def test_generate_16_seats():
    seats = generate_seat_labels(16)
    assert seats[0] == "A1"
    assert seats[-1] == "D4"
    assert len(seats) == 16


def test_generate_18_seats():
    seats = generate_seat_labels(18)
    assert seats[-2:] == ["E1", "E2"]
    assert len(seats) == 18


def test_generate_zero_seats():
    seats = generate_seat_labels(0)
    assert seats == []


def test_generate_custom_seats_per_row():
    seats = generate_seat_labels(6, seats_per_row=3)
    assert seats == ["A1", "A2", "A3", "B1", "B2", "B3"]