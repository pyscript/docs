"""
Main thread: MicroPython handling the UI.
"""
from pyscript import when, workers
from pyscript.web import page


# Track whether computation is running.
computing = False


@when("click", "#find-btn")
async def find_primes(event):
    """
    Ask the worker to find primes.
    """
    global computing
    
    find_btn = page["#find-btn"]
    stop_btn = page["#stop-btn"]
    limit_input = page["#limit"]
    output = page["#output"]
    
    # Get and validate the limit.
    try:
        limit = int(limit_input.value)
        if limit < 10 or limit > 1000000:
            output.content = "Please enter a number between 10 and 1,000,000"
            return
    except ValueError:
        output.content = "Please enter a valid number"
        return
    
    # Check if numpy should be used.
    use_numpy = page["#use-numpy"].checked
    
    # Update UI state.
    computing = True
    find_btn.disabled = True
    stop_btn.disabled = False
    limit_input.disabled = True
    output.content = f"Computing primes up to {limit:,}..."
    
    try:
        # Get the worker and call its exported function.
        worker = await workers["primes"]
        
        # Time the computation.
        import time
        start = time.time()
        result = await worker.find_primes(limit, use_numpy)
        elapsed = time.time() - start
        
        if computing:
            # Convert to string properly.
            first_20 = result['first_20']
            primes_str = ", ".join(str(p) for p in first_20)
            
            method = "NumPy" if use_numpy else "Pure Python"
            output.content = f"Found {result['count']:,} primes up to {limit:,}!\n\nMethod: {method}\nTime: {elapsed:.3f} seconds\n\nFirst 20: {primes_str}"
    except Exception as e:
        output.content = f"Error: {e}"
    finally:
        # Reset UI state.
        computing = False
        find_btn.disabled = False
        stop_btn.disabled = True
        limit_input.disabled = False


@when("click", "#stop-btn")
def stop_computation(event):
    """
    Stop the computation (sets flag, doesn't actually interrupt worker).
    """
    global computing
    
    computing = False
    
    output = page["#output"]
    output.content = "Stopped (worker completed, but result discarded)"
    
    find_btn = page["#find-btn"]
    stop_btn = page["#stop-btn"]
    limit_input = page["#limit"]
    
    find_btn.disabled = False
    stop_btn.disabled = True
    limit_input.disabled = False