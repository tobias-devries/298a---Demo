import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_counter_full(dut):
    """Test all features of the 8-bit programmable counter."""
    
    # 1. Start a 100MHz clock (10ns period)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut._log.info("Starting Counter Cocotb Test...")

    # 2. Apply Asynchronous Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    
    # Verify counter resets to 0
    assert dut.uo_out.value == 0, f"Reset failed! Expected 0, got {dut.uo_out.value}"
    
    # Release Reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # 3. Test Synchronous Load
    test_load_val = 50
    dut._log.info(f"Loading parallel value: {test_load_val}")
    dut.ui_in.value = test_load_val   # Set input bus data
    dut.uio_in.value = 1              # Set load bit high (uio_in[0])
    await ClockCycles(dut.clk, 1)     # Wait for clock edge to load

    # Disable load to resume counting
    dut.uio_in.value = 0
    
    # Verify loaded value
    assert dut.uo_out.value == test_load_val, f"Load failed! Expected {test_load_val}, got {dut.uo_out.value}"

    # 4. Test Up-Counting
    dut._log.info("Testing sequential up-counting...")
    await ClockCycles(dut.clk, 5)
    expected_val = test_load_val + 5
    assert dut.uo_out.value == expected_val, f"Counting failed! Expected {expected_val}, got {dut.uo_out.value}"

    # 5. Test Overflow / Rollover (255 -> 0)
    dut._log.info("Testing overflow wrap-around...")
    dut.ui_in.value = 255
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 1)     # Load 255
    
    dut.uio_in.value = 0              # Clear load
    await ClockCycles(dut.clk, 1)     # Count up by 1 (should roll over to 0)

    assert dut.uo_out.value == 0, f"Overflow failed! Expected 0, got {dut.uo_out.value}"

    dut._log.info("All counter tests passed successfully!")
