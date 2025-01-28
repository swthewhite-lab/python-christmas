from unittest.mock import patch
from io import StringIO
import os

import pytest

from christmas.main import main


def run_io_fun(inputs):
    """
    inputs: 리스트 형태로, 각 줄에 입력할 값을 순서대로 담는다.
    예) ["3", "티본스테이크-1,바비큐립-1,초코케이크-2,제로콜라-1"]
    """
    with patch("builtins.input", side_effect=inputs):
        buffer = StringIO()
        with patch("sys.stdout", new=buffer):
            main()
        outputs = buffer.getvalue()
    return outputs


line_separator = os.linesep


def test_모든_타이틀_출력():
    outputs = run_io_fun(["3", "티본스테이크-1,바비큐립-1,초코케이크-2,제로콜라-1"])
    assert all(
        expected_output in outputs
        for expected_output in [
            "<주문 메뉴>",
            "<할인 전 총주문 금액>",
            "<증정 메뉴>",
            "<혜택 내역>",
            "<총혜택 금액>",
            "<할인 후 예상 결제 금액>",
            "<12월 이벤트 배지>",
        ]
    )


def test_혜택_내역_없음_출력():
    outputs = run_io_fun(["26", "타파스-1,제로콜라-1"])
    assert "<혜택 내역>" + line_separator + "없음" in outputs


def test_날짜_예외_테스트():
    outputs = run_io_fun(["a"])
    assert "[ERROR] 유효하지 않은 날짜입니다. 다시 입력해 주세요." in outputs


def test_주문_예외_테스트():
    outputs = run_io_fun(["3", "제로콜라-a"])
    assert "[ERROR] 유효하지 않은 주문입니다. 다시 입력해 주세요." in outputs
