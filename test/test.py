import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test()
async def test_counter_full(dut):
    """Test all features of the 8-bit programmable counter."""

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut._log.info("Starting Counter Cocotb Test...")

    # Initial values
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # Reset
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 0, \
        f"Reset failed! Expected 0, got {dut.uo_out.value}"

    # Release reset
    dut.rst_n.value = 1

    # --------------------------------------------------
    # LOAD 50
    # --------------------------------------------------
    test_load_val = 50

    dut._log.info(f"Loading parallel value: {test_load_val}")

    dut.ui_in.value = test_load_val
    dut.uio_in.value = 1

    # The next rising edge performs the load
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == test_load_val, \
        f"Load failed! Expected {test_load_val}, got {dut.uo_out.value}"

    # Turn load off
    dut.uio_in.value = 0

    # --------------------------------------------------
    # COUNT UP
    # --------------------------------------------------
    dut._log.info("Testing sequential up-counting...")

    for _ in range(5):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")

    expected_val = test_load_val + 5

    assert dut.uo_out.value == expected_val, \
        f"Counting failed! Expected {expected_val}, got {dut.uo_out.value}"

    # --------------------------------------------------
    # LOAD 255
    # --------------------------------------------------
    dut._log.info("Testing overflow wrap-around...")

    dut.ui_in.value = 255
    dut.uio_in.value = 1

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 255, \
        f"255 load failed! Expected 255, got {dut.uo_out.value}"

    # Disable load
    dut.uio_in.value = 0

    # 255 + 1 -> 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 0, \
        f"Overflow failed! Expected 0, got {dut.uo_out.value}"

    dut._log.info("All counter tests passed successfully!")
